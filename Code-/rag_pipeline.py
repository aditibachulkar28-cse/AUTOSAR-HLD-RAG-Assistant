from .prompts import build_prompt
from .llm_provider import generate

def answer_question(question, embedder, store, top_k=4):
    if not question or not question.strip(): raise ValueError("Please enter a question.")
    evidence = store.search(embedder.encode([question])[0], top_k)
    if not evidence: return {"answer": "I could not find sufficient evidence for this answer in the uploaded HLD.", "evidence": [], "mode": "demo"}
    context = "\n\n".join(f"[Source: {e['source']}, Page {e['page']}, Section: {e['section']}]\n{e['text']}" for e in evidence)
    answer, mode = generate(build_prompt(question, context), evidence)
    citations = " ".join(f"[Source: {e['source']}, Page {e['page']}, Section: {e['section']}]" for e in evidence)
    return {"answer": f"{answer}\n\n{citations}", "evidence": evidence, "mode": mode}
