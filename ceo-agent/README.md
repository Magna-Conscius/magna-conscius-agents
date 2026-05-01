# CEO Agent CLI

This folder gives you a practical command-line CEO agent for Magna Conscius.

## Files
- `ceo_system_prompt.md` - CEO role and response schema
- `ceo_state.json` - current org context and KPIs
- `chat_ceo.py` - chat runner
- `chat_log.jsonl` - auto-generated message history

## Quick Start
Run from repo root:

```powershell
python magna-conscius-agents/ceo-agent/chat_ceo.py --message "Plan this week for first supermarket pilot"
```

Default behavior is `--provider auto`, which now prefers **Ollama**.
With your setup, that means it will use `qwen3.5:0.8b` as the fast CEO agent.

## Providers

```powershell
python magna-conscius-agents/ceo-agent/chat_ceo.py --provider ollama --ollama-model qwen3.5:0.8b --message "What are today's priorities?"
python magna-conscius-agents/ceo-agent/chat_ceo.py --provider openai --model gpt-5.4 --message "Route this quarter goals to agents"
python magna-conscius-agents/ceo-agent/chat_ceo.py --provider local --message "Fallback planning mode"
```

## Deep Research Pattern
- Fast orchestration: `--provider ollama` with `qwen3.5:0.8b`
- High-stakes/deep research decisions: `--provider openai` with a stronger cloud model

## Keep It Useful
- Update `ceo_state.json` weekly.
- Keep KPI fields current.
- Use structured asks, for example:
  - "Prioritize next 7 days to close first pilot."
  - "Create delegations for Research, Sales, and Training agents."
