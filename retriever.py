"""M3: Retrieval over the breed corpus.

BGE-M3 dense+sparse+colbert, weighted fusion (0.4/0.2/0.4 — docs/en.md
Step 3 weights from the 05-22 lesson), searched over CHILD chunks, resolved
to PARENT sections (the unit handed to the LLM). One model load, cached.
"""
import numpy as np
from FlagEmbedding import BGEM3FlagModel

from corpus import build_index

_MODEL = None
FUSION = {"dense": 0.4, "sparse": 0.2, "colbert": 0.4}


def get_encoder():
    global _MODEL
    if _MODEL is None:
        _MODEL = BGEM3FlagModel("BAAI/bge-m3", use_fp16=False)
    return _MODEL


def _norm(vecs):
    arr = np.asarray(vecs)
    return arr / (np.linalg.norm(arr, axis=-1, keepdims=True) + 1e-12)


def _dense_scores(q_dense, d_dense):
    return _norm(q_dense) @ _norm(d_dense).T  # (n_q, n_d)


def _sparse_scores(q_lex, d_lex):
    """Sum q_w * d_w over shared tokens (BGE-M3 lexical weights dicts)."""
    out = np.zeros((len(q_lex), len(d_lex)))
    for i, qd in enumerate(q_lex):
        for j, dd in enumerate(d_lex):
            out[i, j] = sum(w * dd.get(t, 0.0) for t, w in qd.items())
    return out


def _colbert_scores(q_col, d_col):
    """Max-sim sum: query token's best doc token, summed over query tokens."""
    out = np.zeros((len(q_col), len(d_col)))
    for i, qv in enumerate(q_col):
        q = _norm(qv)                       # (n_qtok, dim)
        for j, dv in enumerate(d_col):
            d = _norm(dv)                   # (n_dtok, dim)
            out[i, j] = float((q @ d.T).max(axis=1).sum())
    return out


def _minmax(m):
    lo, hi = m.min(axis=1, keepdims=True), m.max(axis=1, keepdims=True)
    return (m - lo) / (hi - lo + 1e-12)


def fuse_scores(dense, sparse, colbert):
    """Per-row min-max normalize each mode, then weighted sum (0.4/0.2/0.4)."""
    return (FUSION["dense"] * _minmax(dense)
            + FUSION["sparse"] * _minmax(sparse)
            + FUSION["colbert"] * _minmax(colbert))


class BreedRetriever:
    """Index the corpus children once; answer queries with parent sections."""

    def __init__(self, docs_dir=None):
        self.parents = build_index(docs_dir) if docs_dir else build_index()
        self.children = []       # flat child texts
        self.child_owner = []    # parent index per child
        for pi, p in enumerate(self.parents):
            for c in p.children:
                self.children.append(c)
                self.child_owner.append(pi)
        enc = get_encoder()
        out = enc.encode(self.children, return_dense=True, return_sparse=True,
                         return_colbert_vecs=True)
        self.out = out
        print(f"[retriever] indexed {len(self.children)} children "
              f"over {len(self.parents)} parents")

    def search(self, query, top_k=5, breed=None):
        """Return ranked [(score, parent)] with duplicates removed.

        breed: restrict candidates to one breed's docs (the identified dog).
        """
        enc = get_encoder()
        q = enc.encode([query], return_dense=True, return_sparse=True,
                       return_colbert_vecs=True)
        dense = _dense_scores(q["dense_vecs"], self.out["dense_vecs"])
        sparse = _sparse_scores(q["lexical_weights"], self.out["lexical_weights"])
        colbert = _colbert_scores(q["colbert_vecs"], self.out["colbert_vecs"])
        fused = fuse_scores(dense, sparse, colbert)[0]  # single query row
        if breed:
            mask = [i for i, pi in enumerate(self.child_owner)
                    if self.parents[pi].breed == breed]
        else:
            mask = list(range(len(self.children)))
        order = sorted(mask, key=lambda ci: -fused[ci])
        results, seen = [], set()
        for ci in order:
            pi = self.child_owner[ci]
            if pi in seen:
                continue
            seen.add(pi)
            results.append((float(fused[ci]), self.parents[pi]))
            if len(results) >= top_k:
                break
        return results


def demo():
    r = BreedRetriever()
    for q, want_breed, want_section in [
        ("how much exercise does a golden retriever need?", "golden_retriever", "Exercise"),
        ("common health problems in dachshunds", "dachshund", "Health"),
        ("how often should I brush a poodle's coat", "poodle", "Grooming"),
    ]:
        top = r.search(q, top_k=3)
        hit = any(p.breed == want_breed and p.section == want_section
                  for _, p in top)
        print(f"{'HIT ' if hit else 'MISS'} {q}")
        for s, p in top:
            print(f"   {s:.3f}  {p.source}")


if __name__ == "__main__":
    demo()