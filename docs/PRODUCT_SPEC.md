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

## GMGN-inspired detail model

Dyanto AlphaRadar mirrors useful GMGN-style concepts without depending on private GMGN APIs:

- security checks: liquidity depth, sell pressure, volume/liquidity churn, liquidity/FDV support
- pool profile: DEX, pair address, pair age, active pool count, volume/liquidity ratio
- timeframe tape: 5m, 1h, 6h, 24h price/volume/transaction slices
- smart money panel: placeholder for smart-degen/KOL/fresh-wallet/sniper enrichment
- holder snapshot: placeholder for top holders, dev wallet, LP/pool authority, concentration risk
- research checklist: first 70 buyers, pool authority separation, liquidity lock/burn, smart money accumulation, dust pool filtering


## Network roadmap

Current production focus is Solana-first. Coming soon networks:

- Base
- Ethereum
- TON

Each network should reuse the same high-level pipeline while adding chain-specific adapters for DEX data, pool authority checks, holder concentration, wallet-role classification, and security signals.

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
