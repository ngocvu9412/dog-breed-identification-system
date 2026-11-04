"""M5: Eval harness — gold-anchored protocol (05-23 conventions).

Gold lives in SOURCE-DOC coordinates (breed slug + section), never in
chunk indices. Three resolvers grade a ranked parent list:
  - owners:  top-k parent's breed+section == gold breed+section
  - breed:   top-k parent's breed == gold breed (coarser)
  - span:    gold fact substring appears in a top-k parent's text

Metrics: recall@k (gold anywhere in top-k) + MRR (rank of first hit).
Answer-level faithfulness: does the generated answer contain the gold fact
span (exact or the gold's key phrase)?
"""
import json
import re
import time

from corpus import build_index

GOLD_SET = [
    # (query, breed_slug, section, gold_fact_substring)
    ("how much exercise does a golden retriever need?",
     "golden_retriever", "Exercise", "1-2 hours of activity daily"),
    ("common health problems in dachshunds",
     "dachshund", "Health", "intervertebral disc disease"),
    ("how often should I brush a poodle's coat",
     "poodle", "Grooming", "every 4-6 weeks"),
    ("what health issues affect french bulldogs",
     "french_bulldog", "Health", "heat intolerance"),
    ("are border collies good with children",
     "border_collie", "Temperament", "raised with them"),
    ("do huskies shed a lot",
     "siberian_husky", "Grooming", "coat blows"),
    ("how long do chihuahuas live",
     "chihuahua", "Health", "14-17 years"),
    ("is a rottweiler a good family dog",
     "rottweiler", "Temperament", "gentle"),
    ("do pugs have breathing problems",
     "pug", "Health", "Brachycephalic"),
    ("how much grooming does a shih tzu need",
     "shih_tzu", "Grooming", "daily brushing"),
    ("what were pomeranians bred for",
     "pomeranian", "Overview", "sled dogs"),
    ("can great danes run long distances",
     "great_dane", "Exercise", "No forced running"),
    ("are beagles easy to train",
     "beagle", "Temperament", "The nose rules"),
    ("how big do german shepherds get",
     "german_shepherd", "Overview", "30-40 kg"),
    ("do yorkshire terriers shed",
     "yorkshire_terrier", "Overview", "grows continuously"),
    ("what group is the boston terrier in",
     "boston_terrier", "Overview", "Non-Sporting"),
    ("how much exercise does a dobermann need daily",
     "dobermann", "Exercise", "1-2 hours"),
    ("are australian shepherds smart",
     "australian_shepherd", "Temperament", "Brilliant"),
    ("what colors do boxers come in",
     "boxer", "Overview", "fawn or brindle"),
    ("do shetland sheepdogs bark a lot",
     "shetland_sheepdog", "Temperament", "vocal"),
]


def resolve_hit(parent, gold_breed, gold_section, gold_span):
    """Owner-level hit: parent is the gold breed+section, or contains span."""
    if parent.breed == gold_breed and parent.section == gold_section:
        return True
    if gold_span and gold_span.lower() in parent.text.lower():
        return True
    return False


def evaluate_retrieval(retriever, gold_set=GOLD_SET, top_k=5, verbose=True):
    """Recall@k + MRR at parent level (owners resolver)."""
    recalls, rranks = [], []
    for query, gb, gs, span in gold_set:
        ranked = retriever.search(query, top_k=top_k)
        rank = None
        for i, (_, p) in enumerate(ranked, start=1):
            if resolve_hit(p, gb, gs, span):
                rank = i
                break
        recalls.append(rank is not None)
        rranks.append(1.0 / rank if rank else 0.0)
        if verbose:
            mark = f"hit@{rank}" if rank else "MISS"
            print(f"  {mark:7s} {query[:52]:52s} -> "
                  + (ranked[0][1].source if ranked else "none"))
    return sum(recalls) / len(recalls), sum(rranks) / len(rranks)


def evaluate_answers(retriever, generator, gold_set=GOLD_SET, top_k=5,
                     limit=None, verbose=True):
    """Answer-level faithfulness: gold span (or its key phrase) in answer."""
    results = []
    cases = gold_set[:limit] if limit else gold_set
    for query, gb, gs, span in cases:
        ranked = retriever.search(query, top_k=top_k)
        answer, cites = generator.generate(query, ranked)
        # faithfulness: the answer contains the gold span or its core phrase
        # (normalize unicode dashes: models often emit '14–17' en-dash)
        norm = lambda s: s.replace("\u2013", "-").replace("\u2014", "-").lower()
        key = norm(span).split(" of ")[0].strip()
        faithful = norm(span) in norm(answer) or key in norm(answer)
        results.append({"query": query, "gold": f"{gb}#{gs}",
                        "answer": answer, "cites": cites,
                        "faithful": faithful})
        if verbose:
            print(f"  {'FAITH' if faithful else 'DRIFT '} {query[:52]}")
        time.sleep(1.0)  # be polite to the API
    frac = sum(r["faithful"] for r in results) / len(results)
    return frac, results


def save_report(recall, mrr, faith, results, path="eval_report.json"):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"recall@5": recall, "mrr": mrr,
                   "faithfulness": faith,
                   "n_gold": len(results) if results else len(GOLD_SET),
                   "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "results": results}, f, indent=2, ensure_ascii=False)
    print(f"report -> {path}")


if __name__ == "__main__":
    import sys
    import retriever
    import generator

    r = retriever.BreedRetriever()
    print("== retrieval eval (owners resolver, gold in source-doc coords) ==")
    recall, mrr = evaluate_retrieval(r, top_k=5)
    print(f"recall@5 = {recall:.3f}   MRR = {mrr:.3f}")

    faith = None
    results = []
    if "--answers" in sys.argv:
        print("== answer-level eval (glm-5.3, slower) ==")
        faith, results = evaluate_answers(r, generator, limit=10)
        print(f"faithfulness = {faith:.3f}")

    save_report(recall, mrr, faith, results)