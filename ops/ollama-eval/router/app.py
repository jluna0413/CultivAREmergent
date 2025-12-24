from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import time

app = FastAPI(title="Model Router")

# Default Ollama endpoint used in this workspace
OLLAMA_ENDPOINT = "http://127.0.0.1:11436/v1"


class RouteRequest(BaseModel):
    prompt: str
    task: str = "general"  # math, translate, summarize, general
    max_tokens: int = 256
    timeout_sec: int = 120


def choose_model(task: str):
    """Return (model_id, temperature) for a given task."""
    task = (task or "").lower()
    if task == "math":
        return ("gemma3:1b", 0.7)
    if task == "translate":
        return ("gemma3:1b", 0.7)
    if task == "summarize":
        return ("cogito:3b-v1-preview-llama-q4_K_M", 0.0)
    # default fallback
    return ("gemma3:270m", 0.0)


async def call_ollama(model: str, prompt: str, temperature: float, max_tokens: int, timeout_sec: int):
    url = OLLAMA_ENDPOINT.rstrip("/") + "/completions"
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": int(max_tokens)
    }
    if temperature is not None:
        payload["temperature"] = float(temperature)

    start = time.time()
    async with httpx.AsyncClient(timeout=timeout_sec) as client:
        r = await client.post(url, json=payload)
        elapsed = int((time.time() - start) * 1000)
        if r.status_code < 200 or r.status_code >= 300:
            return {"error": f"HTTP {r.status_code}", "raw": r.text, "elapsed_ms": elapsed, "status_code": r.status_code}
        try:
            body = r.json()
        except Exception:
            body = r.text

    # try to extract text similar to evaluator
    response_text = None
    if isinstance(body, dict):
        if "choices" in body and isinstance(body["choices"], list) and len(body["choices"]) > 0:
            c = body["choices"][0]
            response_text = c.get("text") or c.get("message") or None
        if not response_text and body.get("text"):
            response_text = body.get("text")
        if not response_text and body.get("output"):
            out = body.get("output")
            if isinstance(out, list) and len(out) > 0:
                item = out[0]
                if isinstance(item, dict):
                    response_text = item.get("text") or item.get("message") or None
            elif isinstance(out, dict):
                response_text = out.get("text") or None
    elif isinstance(body, list) and len(body) > 0:
        first = body[0]
        if isinstance(first, dict) and first.get("text"):
            response_text = first.get("text")

    return {"response_text": response_text, "raw": body, "elapsed_ms": elapsed, "status_code": r.status_code}


@app.post("/route")
async def route(req: RouteRequest):
    model, temp = choose_model(req.task)

    # Call primary model
    primary = await call_ollama(model, req.prompt, temp, req.max_tokens, req.timeout_sec)
    # If primary produced an empty response or error, call fallback (gemma3:270m)
    if (primary.get("response_text") is None or primary.get("response_text").strip() == "") and (primary.get("status_code") == 200):
        fallback_model, fallback_temp = ("gemma3:270m", 0.0)
        fb = await call_ollama(fallback_model, req.prompt, fallback_temp, req.max_tokens, req.timeout_sec)
        return {
            "model": model,
            "temperature": temp,
            "response": primary.get("response_text"),
            "primary_raw": primary.get("raw"),
            "fallback": {
                "model": fallback_model,
                "temperature": fallback_temp,
                "response": fb.get("response_text"),
                "raw": fb.get("raw"),
                "elapsed_ms": fb.get("elapsed_ms")
            },
            "elapsed_ms": primary.get("elapsed_ms")
        }

    return {"model": model, "temperature": temp, "response": primary.get("response_text"), "raw": primary.get("raw"), "elapsed_ms": primary.get("elapsed_ms")}


@app.get("/health")
async def health():
    # quick check to Ollama models endpoint
    url = OLLAMA_ENDPOINT.rstrip("/") + "/models"
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url)
            if r.status_code == 200:
                return {"ok": True, "models_len": len(r.json().get("data", []))}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    return {"ok": False, "status": r.status_code}
