"""M4: Generation with glm-5.3 (ollama-cloud) — grounded answers.

The retrieved parent sections are injected into the prompt as numbered
context blocks; the model must answer ONLY from them and cite the numbers.
"""
import json
import os
import urllib.request

# ollama-cloud key from hermes .env (never hardcoded)
ENV_PATH = os.path.join(os.environ.get("APPDATA", ""), "..", "Local", "hermes", ".env")


def _api_key():
    env = os.environ.get("OLLAMA_API_KEY")
    if env:
        return env
    for cand in (os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local", "hermes", ".env"),
                 os.environ.get("USERPROFILE", "") + "\\.env"):
        if cand and os.path.exists(cand):
            with open(cand, encoding="utf-8") as f:
                for line in f:
                    if line.startswith("OLLAMA_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"')
    raise RuntimeError("OLLAMA_API_KEY not found in environment or hermes .env")


BASE_URL = "https://ollama.com/v1"
MODEL = "glm-5.3"

SYSTEM = (
    "You are a dog-breed expert assistant. Answer ONLY from the numbered "
    "context blocks provided. Cite every fact as [n] matching the block "
    "number. If the context does not answer the question, say so plainly. "
    "Be concise: 2-6 sentences."
)


def build_prompt(question, retrieved):
    """retrieved = [(score, ParentChunk)] -> grounded prompt."""
    blocks = []
    for n, (_, p) in enumerate(retrieved, start=1):
        blocks.append(f"[{n}] {p.source}\n{p.text}")
    context = "\n\n".join(blocks)
    return (
        f"Context sections about dog breeds:\n\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer using only the context above. Cite blocks as [n]."
    )


def generate(question, retrieved, timeout=120):
    """Call glm-5.3 and return (answer_text, citations_used)."""
    prompt = build_prompt(question, retrieved)
    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
    }).encode("utf-8")
    req = urllib.request.Request(
        BASE_URL + "/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {_api_key()}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = json.load(r)
    answer = body["choices"][0]["message"]["content"]
    import re
    cites = sorted({int(m) for m in re.findall(r"\[(\d+)\]", answer)})
    return answer, cites


if __name__ == "__main__":
    # smoke test with fake retrieved chunks (no retriever needed)
    from corpus import ParentChunk
    fake = [(0.9, ParentChunk(breed="golden_retriever", section="Exercise",
                              text="Needs 1-2 hours of activity daily: walks, fetch, or swimming.")),
            (0.5, ParentChunk(breed="golden_retriever", section="Health",
                              text="Typical lifespan 10-12 years."))]
    ans, cites = generate("How much exercise does a golden retriever need?", fake)
    print("ANSWER:", ans)
    print("CITES:", cites)