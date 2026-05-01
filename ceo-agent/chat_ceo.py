#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.request
from datetime import UTC, datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROMPT_PATH = BASE_DIR / "ceo_system_prompt.md"
STATE_PATH = BASE_DIR / "ceo_state.json"
LOG_PATH = BASE_DIR / "chat_log.jsonl"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def append_log(entry: dict) -> None:
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=True) + "\n")


def local_ceo_response(user_message: str, state: dict) -> dict:
    today = datetime.now(UTC).date().isoformat()
    priorities = [
        {
            "title": "Book first 3 supermarket manager meetings",
            "owner": "Founder + Sales Agent",
            "deadline": today,
            "why": "No pilot can start without discovery meetings."
        },
        {
            "title": "Launch a 4-week founding pilot offer",
            "owner": "Client Success Agent",
            "deadline": today,
            "why": "Need first measurable outcome case study."
        },
        {
            "title": "Publish 5 frontline behavior content pieces this week",
            "owner": "Insight Agent",
            "deadline": today,
            "why": "Build authority while pipeline is being opened."
        }
    ]
    return {
        "summary": f"Local mode response for: {user_message[:120]}",
        "priorities": priorities,
        "delegations": [
            {
                "to": "Research Agent",
                "task": "Map top 20 supermarkets in target region and classify by branch count.",
                "expected_output": "Prioritized target list with contact paths.",
                "deadline": today
            },
            {
                "to": "Training Agent",
                "task": "Draft first 8 micro-lessons for cashier and floor staff conflict scenarios.",
                "expected_output": "Lesson scripts + quick assessment rubric.",
                "deadline": today
            }
        ],
        "risks": [
            {
                "risk": "Trying to build full app before validating pilot demand.",
                "severity": "high",
                "mitigation": "Sell and run pilot first; app scope follows validated pain points."
            }
        ],
        "escalations": [
            {
                "decision": "Approve founding pilot discount floor",
                "reason": "Pricing guardrail required before outreach."
            }
        ],
        "kpi_focus": [
            {"metric": "meetings_booked_weekly", "target": ">=3", "current": str(state.get("kpis", {}).get("meetings_booked_weekly", "unknown"))},
            {"metric": "pilot_clients_active", "target": ">=1", "current": str(state.get("kpis", {}).get("pilot_clients_active", "unknown"))}
        ],
        "questions": [
            "Which city/region should be the first supermarket pilot market?"
        ]
    }


def call_openai(system_prompt: str, state: dict, user_message: str, model: str) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set.")

    payload = {
        "model": model,
        "input": [
            {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
            {"role": "system", "content": [{"type": "input_text", "text": "CEO state:\n" + json.dumps(state, ensure_ascii=True)}]},
            {"role": "user", "content": [{"type": "input_text", "text": user_message}]}
        ]
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=90) as resp:
        raw = resp.read().decode("utf-8")
        parsed = json.loads(raw)

    text = parsed.get("output_text", "").strip()
    if not text:
        raise RuntimeError("No output_text returned by model.")

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Model did not return valid JSON: {exc}\nRaw output:\n{text}") from exc


def call_ollama(system_prompt: str, state: dict, user_message: str, model: str, host: str) -> dict:
    payload = {
        "model": model,
        "prompt": (
            f"{system_prompt}\n\n"
            f"CEO state:\n{json.dumps(state, ensure_ascii=True)}\n\n"
            f"User message:\n{user_message}\n\n"
            "Return only valid JSON matching the required schema."
        ),
        "stream": False
    }
    data = json.dumps(payload).encode("utf-8")
    base = host.rstrip("/")
    req = urllib.request.Request(
        f"{base}/api/generate",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        raw = resp.read().decode("utf-8")
        parsed = json.loads(raw)
    text = (parsed.get("response") or "").strip()
    if not text:
        raise RuntimeError("No response returned by Ollama.")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Ollama did not return valid JSON: {exc}\nRaw output:\n{text}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Chat with Magna Conscius CEO Agent.")
    parser.add_argument("--message", required=True, help="Message to the CEO agent.")
    parser.add_argument("--provider", choices=["auto", "ollama", "openai", "local"], default="auto")
    parser.add_argument("--mode", choices=["auto", "live", "local"], default="auto", help="Deprecated. Use --provider.")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-5.4"))
    parser.add_argument("--ollama-model", default=os.getenv("OLLAMA_MODEL", "qwen3.5:0.8b"))
    parser.add_argument("--ollama-host", default=os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434"))
    args = parser.parse_args()

    if not PROMPT_PATH.exists() or not STATE_PATH.exists():
        print("Missing ceo_system_prompt.md or ceo_state.json", file=sys.stderr)
        return 1

    system_prompt = read_text(PROMPT_PATH)
    state = read_json(STATE_PATH)
    provider = args.provider
    if provider == "auto":
        # Backward compatibility path for old --mode usage
        if args.mode == "live":
            provider = "openai"
        elif args.mode == "local":
            provider = "local"
        else:
            provider = "ollama"

    fallback_note = None
    try:
        if provider == "openai":
            response = call_openai(system_prompt, state, args.message, args.model)
        elif provider == "ollama":
            try:
                response = call_ollama(
                    system_prompt,
                    state,
                    args.message,
                    args.ollama_model,
                    args.ollama_host,
                )
            except Exception as ollama_exc:
                fallback_note = f"Ollama fallback to local mode: {ollama_exc}"
                response = local_ceo_response(args.message, state)
        else:
            response = local_ceo_response(args.message, state)
    except Exception as exc:
        print(f"CEO agent error: {exc}", file=sys.stderr)
        return 2

    if fallback_note:
        response.setdefault("risks", []).append(
            {
                "risk": fallback_note,
                "severity": "medium",
                "mitigation": "Check Ollama service health and model performance."
            }
        )

    event = {
        "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "mode": provider if not fallback_note else f"{provider}->local",
        "message": args.message,
        "response": response
    }
    append_log(event)
    print(json.dumps(response, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
