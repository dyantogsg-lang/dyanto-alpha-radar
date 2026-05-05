# Dyanto AlphaRadar

Autonomous crypto market intelligence agent for Solana memecoins and DEX opportunities.

Dyanto AlphaRadar turns token addresses, pairs, or market keywords into structured intelligence reports: live market structure, opportunity/risk score, narrative hints, verdict, and dry-run action ideas.

## Why this project

Built as a high-quality agentic showcase for Xiaomi MiMo-style long-context/tool-use workflows.

It is not a simple chatbot. It is an agent workflow:

1. Accepts a token/query.
2. Fetches live DEX data from Dexscreener.
3. Falls back to search when direct token lookup fails.
4. Normalizes liquidity, volume, transaction, price, FDV, and venue data.
5. Scores opportunity and risk.
6. Classifies the move as Organic, Coordinated, Manipulated, Mixed, or Monitor.
7. Renders a readable analyst-style report.
8. Exposes CLI, API, and local dashboard.

## Current features

- Dexscreener adapter
- GeckoTerminal adapter scaffold
- Solana-first pair selection
- Market quality scoring
- Risk flags
- Narrative/social metadata extraction
- Markdown report renderer
- Typer CLI
- FastAPI API
- Minimal web dashboard
- Test suite
- Dry-run only by default

## Install

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
```

## CLI usage

```bash
dyanto-alpha-radar So11111111111111111111111111111111111111112
```

Save report:

```bash
dyanto-alpha-radar <TOKEN_OR_QUERY> -o reports/example.md
```

JSON output:

```bash
dyanto-alpha-radar <TOKEN_OR_QUERY> --json
```

## API / dashboard

```bash
uvicorn dyanto_alpha_radar.api:app --reload --host 127.0.0.1 --port 8787
```

Open:

```text
http://127.0.0.1:8787
```

API:

```text
GET /api/scan?target=<TOKEN_OR_QUERY>
GET /report?target=<TOKEN_OR_QUERY>
```

## Report sections

- What it is
- Live structure
- Score
- Why it moved / narrative
- Verdict
- Risk flags
- Suggested actions
- Safety mode

## Roadmap

- Solana RPC holder concentration module
- Pump.fun fallback
- GeckoTerminal participant breadth enrichment
- Telegram alert publisher
- Open WebUI plugin wrapper
- Backtest/dry-run trade simulator
- Wallet-role classifier: LP/pool authority vs real insiders
- Chart screenshot multimodal analysis
- Scheduled radar watchlists
- Public demo video

## Safety

Dyanto AlphaRadar is dry-run intelligence software. It does not execute live trades by default.

## License

MIT
