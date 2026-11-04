"""Breed classifier: MobileNetV3-large ImageNet, dog classes 151-268.

M1 logic productized: load model once, classify an image, return top-k
predictions restricted to (or flagged for) the dog range. Inference only —
the model is never trained.
"""
from dataclasses import dataclass

import torch
from PIL import Image
from torchvision import models

DOG_RANGE = (151, 268)  # ImageNet class indices that are dog breeds

_MODEL_CACHE: dict = {}


def get_model():
    """Load MobileNetV3-large once and reuse (weights cached by torchvision)."""
    if "model" not in _MODEL_CACHE:
        weights = models.MobileNet_V3_Large_Weights.IMAGENET1K_V2
        _MODEL_CACHE["model"] = models.mobilenet_v3_large(weights=weights).eval()
        _MODEL_CACHE["preprocess"] = weights.transforms()
        _MODEL_CACHE["labels"] = weights.meta["categories"]
    return _MODEL_CACHE["model"], _MODEL_CACHE["preprocess"], _MODEL_CACHE["labels"]


@dataclass
class Prediction:
    label: str          # ImageNet category name
    score: float        # softmax probability
    index: int          # ImageNet class index
    is_dog: bool        # inside DOG_RANGE

    @property
    def slug(self):
        """Map an ImageNet dog label to a corpus doc slug (or None)."""
        return LABEL_TO_SLUG.get(self.label)


def _load_image(path_or_pil):
    if isinstance(path_or_pil, Image.Image):
        return path_or_pil.convert("RGB")
    return Image.open(path_or_pil).convert("RGB")


def classify(path_or_pil, top_k=3):
    """Classify one image; return list[Prediction] sorted by score."""
    model, preprocess, labels = get_model()
    img = _load_image(path_or_pil)
    x = preprocess(img).unsqueeze(0)
    with torch.no_grad():
        probs = torch.nn.functional.softmax(model(x), dim=1)[0]
    top = probs.topk(top_k)
    out = []
    for score, idx in zip(top.values.tolist(), top.indices.tolist()):
        out.append(Prediction(label=labels[idx], score=score, index=idx,
                              is_dog=DOG_RANGE[0] <= idx <= DOG_RANGE[1]))
    return out


def classify_breed(path_or_pil, top_k=3, min_confidence=0.10):
    """Classify and keep only dog predictions.

    Returns (predictions, diagnosis). Diagnosis is one of:
      'ok'       — top-1 is a dog above min_confidence
      'low'      — top-1 dog below min_confidence (top-k candidates offered)
      'not_dog'  — no dog class in top-k
    """
    preds = classify(path_or_pil, top_k=top_k)
    dog_preds = [p for p in preds if p.is_dog]
    if not dog_preds:
        return dog_preds, "not_dog"
    if dog_preds[0].score < min_confidence:
        return dog_preds, "low"
    return dog_preds, "ok"


# ImageNet dog label -> corpus slug. Not every label maps (e.g. 'Eskimo dog'
# has no doc); unmapped labels fall back to the CLI's candidates list.
LABEL_TO_SLUG = {
    "golden retriever": "golden_retriever",
    "Labrador retriever": "labrador_retriever",
    "German shepherd": "german_shepherd",
    "French bulldog": "french_bulldog",
    "standard poodle": "poodle",
    "poodle": "poodle",
    "beagle": "beagle",
    "Rottweiler": "rottweiler",
    "dachshund": "dachshund",
    "wire-haired fox terrier": None,  # no corpus doc — keep explicit
    "Chihuahua": "chihuahua",
    "Great Dane": "great_dane",
    "border collie": "border_collie",
    "Siberian husky": "siberian_husky",
    "Eskimo dog": "siberian_husky",  # husky-type class
    "malamute": None,  # distinct breed, no doc
    "Doberman": "dobermann",
    " boxer": "boxer",
    "boxer": "boxer",
    "Shih-Tzu": "shih_tzu",
    "Pomeranian": "pomeranian",
    "Boston terrier": "boston_terrier",
    "cocker spaniel": "cocker_spaniel",
    "papillon": None,
    "toy terrier": None,
    "Yorkshire terrier": "yorkshire_terrier",
    "Pekinese": None,
    "Chow": None,
    "pug": "pug",
    "Australian shepherd": "australian_shepherd",
    "Shetland sheepdog": "shetland_sheepdog",
    "German short-haired pointer": "german_shorthaired_pointer",
}