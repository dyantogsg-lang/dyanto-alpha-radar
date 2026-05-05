# Dyanto AlphaRadar Product Spec

## One-liner

Autonomous crypto market intelligence agent that detects DEX opportunities, explains why they move, scores risk, and publishes actionable dry-run intelligence.

## Target users

- Crypto researchers
- Memecoin traders
- Telegram alpha communities
- Agent developers evaluating MiMo-style long-context/tool-use agents

## Core workflow

```text
Input token/query
  -> DEX data collection
  -> pair normalization
  -> primary venue selection
  -> market quality score
  -> narrative extraction
  -> verdict classification
  -> report/API/dashboard output
```

## Scoring model

Opportunity subscores:

- liquidity
- volume/liquidity
- transaction breadth
- buy pressure
- momentum
- valuation turnover

Risk flags:

- thin liquidity
- overheated churn
- seller dominance
- parabolic shallow liquidity
- low liquidity/FDV support
- short-term reversal

## Verdict taxonomy

- Organic: broad market quality plus visible narrative
- Coordinated: cluster/call style behavior or holder pressure
- Manipulated: severe holder/market risk with weak organic evidence
- Mixed: real narrative plus coordinated amplification
- Monitor: insufficient conviction

## Demo script

1. Start dashboard.
2. Paste token address or keyword.
3. Show live report.
4. Save markdown report.
5. Explain dry-run only mode.
6. Show roadmap: Solana holder module + Telegram publisher.
