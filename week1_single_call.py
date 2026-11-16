"""Week 1: Single Chat Completions API call using NVIDIA's OpenAI-compatible endpoint."""

import json
import os
from pathlib import Path
import sys

import requests

API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "minimaxai/minimax-m3.1-flash"
DEFAULT_PROMPT = "用一句話說明什麼是 HTTP"


def _load_dotenv(env_path: Path) -> None:
    """Populate os.environ from a local .env file without overriding existing variables."""
    if not env_path.is_file():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if key and key not in os.environ:
            os.environ[key] = value


def call_model(messages: list[dict[str, str]]) -> dict:
    """Send a single Chat Completions request and print status, JSON body, and reply/error."""
    _load_dotenv(Path(__file__).resolve().with_name(".env"))
    api_key = os.environ.get("NVIDIA_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "Missing NVIDIA_API_KEY. Export it in your shell or set it in a local .env file."
        )

    resp = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": messages,
            "max_tokens": 512,
            "temperature": 1,
            "top_p": 0.95,
        },
        timeout=60,
    )
    print("status:", resp.status_code)

    try:
        data = resp.json()
    except ValueError:
        data = {"raw_body": resp.text}

    print(json.dumps(data, ensure_ascii=False, indent=2))

    if resp.ok:
        choices = data.get("choices") or []
        message = (choices[0].get("message") or {}) if choices else {}
        print("reply:", message.get("content"))
    else:
        print("error:", data.get("error", data))

    return data


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]).strip() or DEFAULT_PROMPT
    try:
        call_model([{"role": "user", "content": prompt}])
    except (RuntimeError, requests.RequestException) as exc:
        print(f"request failed: {exc}", file=sys.stderr)
        sys.exit(1)
