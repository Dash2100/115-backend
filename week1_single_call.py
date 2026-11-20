"""Week 1: Single Chat Completions API call using NVIDIA's OpenAI-compatible endpoint."""

import argparse
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
    for raw_line in env_path.read_text(encoding="utf-8-sig").splitlines():
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


def _load_env_files() -> None:
    """Load .env from the script directory and current working directory."""
    script_env = Path(__file__).resolve().with_name(".env")
    cwd_env = Path.cwd() / ".env"
    _load_dotenv(script_env)
    if cwd_env.resolve() != script_env:
        _load_dotenv(cwd_env)


def call_model(messages: list[dict[str, str]], model: str | None = None) -> dict:
    """Send a single Chat Completions request and print status, JSON body, and reply/error."""
    _load_env_files()
    api_key = os.environ.get("NVIDIA_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "Missing NVIDIA_API_KEY. Export it in your shell or set it in a local .env file."
        )

    selected_model = (model or os.environ.get("NVIDIA_MODEL", "")).strip() or MODEL

    resp = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": selected_model,
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
        choices = data.get("choices") if isinstance(data, dict) else None
        first_choice = choices[0] if isinstance(choices, list) and choices else None
        message = first_choice.get("message") if isinstance(first_choice, dict) else None
        content = message.get("content") if isinstance(message, dict) else None
        print("reply:", content)

        usage = data.get("usage") if isinstance(data, dict) else None
        if isinstance(usage, dict):
            print("usage:", json.dumps(usage, ensure_ascii=False))
    else:
        error = data.get("error", data) if isinstance(data, dict) else data
        print("error:", error)

    return data


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send a single Chat Completions API request to NVIDIA's endpoint."
    )
    parser.add_argument(
        "prompt",
        nargs="*",
        help=f"User prompt text (default: {DEFAULT_PROMPT})",
    )
    parser.add_argument(
        "--model",
        default=None,
        help=f"Model ID override (default: NVIDIA_MODEL env var or {MODEL})",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = _parse_args(sys.argv[1:])
    prompt = " ".join(args.prompt).strip() or DEFAULT_PROMPT
    try:
        call_model([{"role": "user", "content": prompt}], model=args.model)
    except (RuntimeError, requests.RequestException) as exc:
        print(f"request failed: {exc}", file=sys.stderr)
        sys.exit(1)
