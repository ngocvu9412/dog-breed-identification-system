# Dog Breed Identification System

Identify a dog's breed from a photo, then answer questions about that
breed with RAG — every answer grounded in the breed's own documentation.

    photo ──> MobileNetV3-large classifier ──> breed label
                                              │
                                              v
              BGE-M3 fusion retrieval over breed docs
                                              │
                                              v
              glm-5.3 grounded answer + [n] citations

## Quick start

    python main.py --image poc/images/German_Shepherd.jpg --ask "how much exercise?"
    python main.py --image poc/images/Pug.jpg                  # classify only
    python main.py --ask "do huskies shed a lot?"              # retrieve only

Setup: `pip install -r requirements.txt` + `OLLAMA_API_KEY` in the
environment (glm-5.3 via https://ollama.com/v1).

## Layout

- `classifier.py` — MobileNetV3-large ImageNet, dog classes 151-268, one
  cached model load. Labels map to corpus slugs; unmapped dog classes are
  reported as candidates.
- `corpus_gen.py` + `docs/` — 23 breed docs, fixed sections
  (Overview / Temperament / Health / Grooming / Exercise / Fun facts).
- `corpus.py` — parent-child chunking: parents = ## sections, children =
  400-char windows, each prefixed with a `breed — section:` context header
  (contextual-retrieval style).
- `retriever.py` — BGE-M3 dense+sparse+colbert, per-row min-max fusion
  0.4/0.2/0.4, search children, return parents; optional `breed=`
  filter restricts to the identified dog's docs.
- `generator.py` — glm-5.3 chat with numbered context blocks; answers must
  cite [n]; abstains when the context does not answer.
- `eval.py` — gold set in source-doc coordinates (breed#section + fact
  span), recall@5 + MRR (owners resolver) and answer-level faithfulness.
- `main.py` — CLI (classify / retrieve / full pipeline).
- `tests/` — pytest unit tests for the pure functions.

## Verified results (2026-11-04)

- Classifier: 5 Wikipedia breed photos, 4/5 top-1 (husky top-2 behind the
  husky-type 'Eskimo dog' class), all predictions in the dog range.
- Retrieval: recall@5 = 1.000, MRR = 0.820 on the 20-gold set.
- Generation: faithfulness 10/10 sample (dash-normalized span matching;
  honest abstention counts against, corpus gaps get fixed, not prompted around).
- Tests: 8/8 pass (`python -m pytest -q tests/`).

## Known limits

- Classifier only knows ImageNet's ~118 dog classes; a breed outside them
  (e.g. 'Eskimo dog' vs husky confusion) surfaces as a candidate list.
- Corpus is 23 breeds; unmapped or unknown breeds retrieve unfiltered.
- glm-5.3 answers are capped at context: it will say so rather than guess.

## Eval

    python eval.py             # retrieval eval (offline, fast)
    python eval.py --answers   # + answer-level faithfulness (glm-5.3, slow)

Reports land in `eval_report.json` + `_answer_eval.log`.