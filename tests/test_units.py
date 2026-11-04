"""Unit tests for the pure functions (no model, no network).

Run:  pytest -q tests/
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from corpus import build_index, chunk_children, load_corpus  # noqa: E402
from eval import resolve_hit, GOLD_SET  # noqa: E402
from classifier import LABEL_TO_SLUG, Prediction, DOG_RANGE  # noqa: E402


def test_corpus_shape():
    parents = build_index()
    # 23 breeds x 6 sections = 138 parents, each with >=1 child
    assert len(parents) == 138, len(parents)
    assert all(p.children for p in parents)
    sections = {p.section for p in parents}
    assert sections == {"Overview", "Temperament", "Health",
                         "Grooming", "Exercise", "Fun facts"}


def test_children_carry_context_header():
    parents = build_index()
    for p in parents:
        for c in p.children:
            assert p.breed.replace("_", " ") in c.lower(), p.source
            break  # first child per parent is enough


def test_child_windowing():
    parents = chunk_children(load_corpus(), child_size=100, overlap=20)
    long = [p for p in parents if len(p.text) > 100]
    assert long, "expected at least one section longer than 100 chars"
    for p in long:
        assert len(p.children) > 1, f"{p.source} should be split into >1 child"


def test_owner_resolution():
    parents = build_index()
    gold = next(p for p in parents
                if p.breed == "golden_retriever" and p.section == "Exercise")
    assert resolve_hit(gold, "golden_retriever", "Exercise", "1-2 hours")
    other = next(p for p in parents
                 if p.breed == "pug" and p.section == "Health")
    assert not resolve_hit(other, "golden_retriever", "Exercise", "1-2 hours")


def test_span_fallback_resolution():
    parents = build_index()
    # wrong breed+section but contains the gold span substring -> hit
    needle = next(p for p in parents if "heat intolerance" in p.text)
    assert resolve_hit(needle, "whatever", "Whatever", "heat intolerance")


def test_label_to_slug_mapping():
    assert LABEL_TO_SLUG["golden retriever"] == "golden_retriever"
    assert LABEL_TO_SLUG["German shepherd"] == "german_shepherd"
    # every mapped slug must exist in the corpus
    parents = build_index()
    slugs = {p.breed for p in parents}
    mapped = {s for s in LABEL_TO_SLUG.values() if s}
    assert mapped <= slugs, mapped - slugs


def test_prediction_dog_flag():
    p_in = Prediction(label="pug", score=0.5, index=255, is_dog=True)
    assert DOG_RANGE[0] <= p_in.index <= DOG_RANGE[1]
    assert p_in.slug == "pug"


def test_gold_set_shape():
    parents = build_index()
    parent_index = {(p.breed, p.section) for p in parents}
    for q, b, s, span in GOLD_SET:
        assert (b, s) in parent_index, f"gold {b}#{s} not in corpus"
        assert isinstance(span, str) and span