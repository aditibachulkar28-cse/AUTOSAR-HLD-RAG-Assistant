"""Optional OpenAI-compatible API, with safe extractive demonstration fallback."""
import json, urllib.request
from .config import LLM_PROVIDER, LLM_API_KEY, LLM_MODEL

def status():
    return "API configured" if LLM_PROVIDER == "openai" and LLM_API_KEY else "Demo extractive mode (no API key required)"

def generate(prompt, evidence):
    if LLM_PROVIDER == "openai" and LLM_API_KEY and LLM_MODEL:
        try:
            payload = json.dumps({"model": LLM_MODEL, "messages": [{"role":"user","content":prompt}], "temperature":0}).encode()
            request = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=payload, headers={"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type":"application/json"})
            with urllib.request.urlopen(request, timeout=45) as response:
                return json.loads(response.read())["choices"][0]["message"]["content"], "api"
        except Exception:
            pass
    # Transparent fallback: show the strongest retrieved passage, never fabricate prose.
    if not evidence: return "I could not find sufficient evidence for this answer in the uploaded HLD.", "demo"
    return "Based on the retrieved HLD evidence: " + evidence[0]["text"][:700], "demo"
