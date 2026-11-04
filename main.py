"""M6: CLI — photo in, grounded answer out.

    python main.py --image poc/images/German_Shepherd.jpg --ask "how much exercise?"
    python main.py --image photo.jpg            # classify only
    python main.py --ask "do huskies shed?"      # retrieve only (no image)
"""
import argparse
import sys


def run(image=None, ask=None, top_k=5, candidates=3):
    # classify if an image is given
    breed_slug = None
    if image:
        from classifier import classify_breed
        dog_preds, diagnosis = classify_breed(image, top_k=candidates)
        print("== breed classification ==")
        for p in dog_preds:
            print(f"  {p.score:.3f}  {p.label}" + ("  *" if p.slug else ""))
        if diagnosis == "not_dog":
            print("no dog detected in this image — nothing to look up.")
            return 1
        if diagnosis == "low":
            print("low confidence; top candidates above. "
                  "try a clearer photo, or ask a general question.")
        top1 = dog_preds[0]
        breed_slug = top1.slug
        if not breed_slug:
            print(f"breed '{top1.label}' has no doc in the corpus; "
                  "asking without breed filter.")
        else:
            print(f"identified: {top1.label} -> {breed_slug}")
        print()

    # retrieve + generate if there is a question
    if ask:
        from retriever import BreedRetriever
        from generator import generate
        r = BreedRetriever()
        # if we know the breed, restrict retrieval to that breed's docs —
        # the answer must be about THAT dog, not generic matches
        ranked = r.search(ask, top_k=top_k, breed=breed_slug)
        print("== retrieved context ==")
        for s, p in ranked:
            print(f"  [{s:.3f}] {p.source}")
        print()
        print("== answer ==")
        answer, cites = generate(ask, ranked)
        print(answer)
        print()
        print("sources: " + ", ".join(
            f"[{n}] {p.source}" for n, (_, p) in enumerate(ranked[:max(cites) if cites else 1], start=1)))
    return 0


def main():
    ap = argparse.ArgumentParser(description="dog breed identification system")
    ap.add_argument("--image", help="path to a dog photo")
    ap.add_argument("--ask", help="question about the breed")
    ap.add_argument("--top-k", type=int, default=5)
    ap.add_argument("--candidates", type=int, default=3)
    args = ap.parse_args()
    if not args.image and not args.ask:
        ap.print_help()
        return 2
    return run(args.image, args.ask, args.top_k, args.candidates)


if __name__ == "__main__":
    sys.exit(main())