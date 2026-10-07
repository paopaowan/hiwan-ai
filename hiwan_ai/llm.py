from __future__ import annotations
from dataclasses import dataclass
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

@dataclass(frozen=True)
class LLMResponse:
    content: str
    thinking: str
    done_reason: str | None
    prompt_eval_count: int
    prompt_eval_duration_ns: int
    eval_count: int
    eval_duration_ns: int

    @property
    def generation_tokens_per_second(self):
        if not self.eval_count or not self.eval_duration_ns:
            return None
        return self.eval_count / (self.eval_duration_ns / 1_000_000_000)

class OllamaClient:
    def __init__(self, model="qwen3.5:27b-mlx", base_url="http://127.0.0.1:11434", timeout_seconds=180.0):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def chat(self, messages, *, think=False, temperature=0.0, num_ctx=8192, num_predict=256, keep_alive="10m"):
        payload = {
            "model": self.model,
            "messages": list(messages),
            "think": think,
            "stream": False,
            "keep_alive": keep_alive,
            "options": {
                "temperature": temperature,
                "num_ctx": num_ctx,
                "num_predict": num_predict,
            },
        }
        req = Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(req, timeout=self.timeout_seconds) as r:
                data = json.load(r)
        except HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            raise RuntimeError(f"Ollama HTTP error {e.code}: {body or e.reason}") from e
        except URLError as e:
            raise RuntimeError(f"Ollama unreachable at {self.base_url}: {e.reason}") from e

        if "error" in data:
            raise RuntimeError(f"Ollama error: {data['error']}")

        msg = data.get("message") or {}
        return LLMResponse(
            content=msg.get("content") or "",
            thinking=msg.get("thinking") or "",
            done_reason=data.get("done_reason"),
            prompt_eval_count=int(data.get("prompt_eval_count") or 0),
            prompt_eval_duration_ns=int(data.get("prompt_eval_duration") or 0),
            eval_count=int(data.get("eval_count") or 0),
            eval_duration_ns=int(data.get("eval_duration") or 0),
        )
