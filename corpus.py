"""Corpus loading + parent-child chunking (05-23 conventions).

Each breed .md becomes: parent chunks (## sections, natural doc units) and
child chunks (fixed-size windows, retrieval units). Retrieval searches
children and returns their owning parent — gold-anchored eval grades at
parent level.
"""
import os
import re
from dataclasses import dataclass, field

DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")


@dataclass
class ParentChunk:
    breed: str           # corpus slug, e.g. 'golden_retriever'
    section: str         # 'Overview', 'Health', ...
    text: str
    children: list = field(default_factory=list)  # child chunk texts

    @property
    def source(self):
        return f"{self.breed}.md#{self.section}"


def load_corpus(docs_dir=DOCS_DIR):
    """Parse every breed .md into parent chunks (one per ## section)."""
    parents = []
    for fname in sorted(os.listdir(docs_dir)):
        if not fname.endswith(".md"):
            continue
        slug = fname[:-3]
        text = open(os.path.join(docs_dir, fname), encoding="utf-8").read()
        # split on ## headers; parts[0] is '# Title' + optional group line
        parts = re.split(r"^## ", text, flags=re.M)
        header = parts[0].strip()
        header_lines = header.split("\n", 1)
        group_text = header_lines[1].strip() if len(header_lines) > 1 else ""
        sections = []
        for part in parts[1:]:
            lines = part.strip().split("\n", 1)
            section = lines[0].strip()
            body = lines[1].strip() if len(lines) > 1 else ""
            sections.append((section, body))
        # merge the group line into the real Overview section (not a new parent)
        if sections and sections[0][0] == "Overview":
            sections[0] = ("Overview", (group_text + "\n\n" + sections[0][1]).strip() if group_text else sections[0][1])
        elif group_text:
            sections.insert(0, ("Overview", group_text))
        for section, body in sections:
            parents.append(ParentChunk(breed=slug, section=section, text=body))
    return parents


def chunk_children(parents, child_size=400, overlap=50):
    """Fixed-size character windows per parent (child chunks).

    Each child is prefixed with a context header (breed + section) so the
    child carries its identity even when the window misses the breed name —
    contextual-retrieval style (05-23 lesson).
    """
    for p in parents:
        text = p.text
        header = f"{p.breed.replace('_', ' ')} — {p.section.lower()}: "
        step = max(1, child_size - overlap)
        i = 0
        while i < len(text):
            window = header + text[i:i + child_size].strip()
            if window.strip():
                p.children.append(window)
            if i + child_size >= len(text):
                break
            i += step
        if not p.children and p.text.strip():
            p.children.append(header + p.text.strip())
    return parents


def build_index(docs_dir=DOCS_DIR, child_size=400, overlap=50):
    """Full pipeline: docs -> parent chunks with children."""
    parents = load_corpus(docs_dir)
    parents = chunk_children(parents, child_size=child_size, overlap=overlap)
    return parents


if __name__ == "__main__":
    ps = build_index()
    n_children = sum(len(p.children) for p in ps)
    print(f"parents: {len(ps)}, children: {n_children}")
    for p in ps[:3]:
        print(f"  {p.source}: {len(p.children)} children, {len(p.text)} chars")
    sections = {}
    for p in ps:
        sections.setdefault(p.section, 0)
        sections[p.section] += 1
    print("sections:", sections)