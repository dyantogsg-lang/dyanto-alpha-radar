from __future__ import annotations

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, PlainTextResponse

from dyanto_alpha_radar.analyzer import analyze
from dyanto_alpha_radar.report import render_markdown_report

app = FastAPI(title="Dyanto AlphaRadar", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "dyanto-alpha-radar"}


@app.get("/api/scan")
async def api_scan(target: str = Query(..., description="Token address, pair, symbol, or search query")) -> dict:
    return await analyze(target)


@app.get("/report", response_class=PlainTextResponse)
async def report(target: str = Query(...)) -> str:
    result = await analyze(target)
    return render_markdown_report(result) if "error" not in result else str(result)


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Dyanto AlphaRadar</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300..900;1,9..40,300..900&display=swap" rel="stylesheet">
  <style>
    :root {
      --blue: #0052ff;
      --blue-2: #2f7dff;
      --cyan: #00c2ff;
      --ink: #07111f;
      --muted: #64748b;
      --line: rgba(15, 23, 42, .10);
      --soft: #f5f8ff;
      --white: #ffffff;
      --green: #10b981;
      --amber: #f59e0b;
      --red: #ef4444;
      --shadow: 0 24px 80px rgba(0, 82, 255, .16);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: 'DM Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(0,82,255,.16), transparent 34rem),
        radial-gradient(circle at 85% 15%, rgba(0,194,255,.13), transparent 28rem),
        linear-gradient(180deg, #ffffff 0%, #f4f8ff 48%, #eef5ff 100%);
    }
    .radar-shell { max-width: 1180px; margin: 0 auto; padding: 28px 24px 48px; }
    .nav { display:flex; align-items:center; justify-content:space-between; gap:16px; margin-bottom:34px; }
    .brand { display:flex; align-items:center; gap:12px; font-weight:800; letter-spacing:-.03em; font-size:20px; }
    .logo {
      width:42px; height:42px; border-radius:16px; display:grid; place-items:center;
      color:white; background:linear-gradient(135deg, var(--blue), var(--cyan)); box-shadow:var(--shadow);
    }
    .status-pill, .verdict-pill {
      display:inline-flex; align-items:center; gap:8px; border:1px solid rgba(0,82,255,.14);
      color:#0640bd; background:rgba(255,255,255,.78); padding:10px 14px; border-radius:999px;
      font-size:13px; font-weight:800; box-shadow:0 10px 30px rgba(15,23,42,.05);
    }
    .dot { width:8px; height:8px; border-radius:99px; background:var(--green); box-shadow:0 0 0 6px rgba(16,185,129,.12); }
    .hero { display:grid; grid-template-columns: 1.05fr .95fr; gap:28px; align-items:stretch; }
    .hero-card, .panel, .metric-card {
      background:rgba(255,255,255,.84); border:1px solid rgba(255,255,255,.7);
      box-shadow:var(--shadow); backdrop-filter: blur(18px); border-radius:32px;
    }
    .hero-card { padding:44px; position:relative; overflow:hidden; }
    .hero-card:after {
      content:""; position:absolute; right:-120px; top:-120px; width:340px; height:340px; border-radius:50%;
      background:radial-gradient(circle, rgba(0,82,255,.15), transparent 65%);
    }
    .eyebrow { color:var(--blue); text-transform:uppercase; letter-spacing:.16em; font-size:12px; font-weight:900; margin-bottom:18px; }
    h1 { font-size: clamp(44px, 7vw, 78px); line-height:.95; letter-spacing:-.075em; margin:0 0 20px; max-width:760px; }
    .lead { color:#40516b; font-size:19px; line-height:1.65; margin:0 0 30px; max-width:680px; }
    .scan-box { display:flex; gap:12px; padding:8px; border:1px solid var(--line); border-radius:999px; background:#ffffff; box-shadow:0 18px 45px rgba(15,23,42,.08); }
    input {
      flex:1; min-width: 0; border:0; outline:0; background:transparent; padding:0 18px;
      font: inherit; color:var(--ink);
    }
    button {
      border:0; border-radius:999px; background:linear-gradient(135deg, var(--blue), var(--blue-2));
      color:#ffffff; font-weight:900; padding:16px 24px; cursor:pointer; box-shadow:0 16px 36px rgba(0,82,255,.25);
      transition: transform .18s ease, box-shadow .18s ease;
    }
    button:hover { transform: translateY(-1px); box-shadow:0 20px 44px rgba(0,82,255,.32); }
    .quick-row { display:flex; gap:10px; flex-wrap:wrap; margin-top:18px; }
    .chip { border:1px solid rgba(0,82,255,.14); background:#f8fbff; color:#174ea6; padding:9px 12px; border-radius:999px; font-size:13px; font-weight:800; cursor:pointer; }
    .visual-card { padding:28px; background:linear-gradient(145deg, #062b7a, #0052ff 58%, #53c7ff); color:#ffffff; border-radius:32px; box-shadow:0 28px 80px rgba(0,82,255,.28); overflow:hidden; position:relative; }
    .visual-card:before { content:""; position:absolute; inset:-40px; background:radial-gradient(circle at 72% 18%, rgba(255,255,255,.36), transparent 22rem); }
    .radar-orb { width:250px; height:250px; border-radius:50%; margin:12px auto 18px; position:relative; border:1px solid rgba(255,255,255,.35); background:radial-gradient(circle, rgba(255,255,255,.28), rgba(255,255,255,.06) 44%, transparent 68%); }
    .radar-orb:after { content:""; position:absolute; inset:24px; border-radius:50%; border:1px dashed rgba(255,255,255,.5); }
    .sweep { position:absolute; left:50%; top:50%; width:45%; height:2px; transform-origin:left center; background:linear-gradient(90deg,#fff,transparent); animation:spin 3.8s linear infinite; }
    @keyframes spin { to { transform:rotate(360deg); } }
    .visual-stats { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; position:relative; }
    .mini { padding:14px; border-radius:20px; background:rgba(255,255,255,.15); border:1px solid rgba(255,255,255,.18); }
    .mini b { display:block; font-size:18px; }
    .mini span { opacity:.8; font-size:12px; }
    .panel { margin-top:28px; padding:28px; }
    .panel-head { display:flex; justify-content:space-between; gap:16px; align-items:center; margin-bottom:20px; }
    .panel h2 { margin:0; font-size:30px; letter-spacing:-.04em; }
    .score-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:20px; }
    .metric-card { padding:20px; border-radius:24px; box-shadow:0 14px 35px rgba(15,23,42,.06); }
    .metric-card span { color:var(--muted); font-size:13px; font-weight:800; text-transform:uppercase; letter-spacing:.08em; }
    .metric-card strong { display:block; font-size:30px; margin-top:8px; letter-spacing:-.05em; }
    .metric-card.opportunity strong { color:var(--blue); }
    .metric-card.risk strong { color:var(--amber); }
    .report-layout { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
    .section-card { border:1px solid var(--line); border-radius:24px; padding:20px; background:#fff; }
    .section-card h3 { margin:0 0 12px; font-size:16px; color:#0f2d5c; }
    .section-card ul { margin:0; padding-left:18px; color:#40516b; line-height:1.6; }
    .gmgn-strip { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:20px 0; }
    .gmgn-card { border:1px solid rgba(0,82,255,.12); border-radius:22px; padding:16px; background:linear-gradient(180deg,#ffffff,#f7faff); }
    .gmgn-card span { display:block; color:var(--muted); font-size:11px; font-weight:900; letter-spacing:.11em; text-transform:uppercase; }
    .gmgn-card b { display:block; margin-top:8px; color:#08265f; font-size:18px; letter-spacing:-.03em; }
    .timeframe-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; }
    .tf { border:1px solid var(--line); border-radius:18px; padding:12px; background:#f8fbff; }
    .tf b { color:var(--blue); }
    pre { white-space:pre-wrap; margin:0; color:#334155; font-size:13px; line-height:1.6; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }
    .loading { color:var(--blue); font-weight:900; }
    .footer { text-align:center; color:#64748b; margin-top:24px; font-size:13px; }
    @media (max-width: 900px) { .hero, .report-layout { grid-template-columns:1fr; } .score-grid { grid-template-columns:repeat(2,1fr); } h1 { font-size:48px; } }
    @media (max-width: 560px) { .radar-shell { padding:18px 14px 32px; } .hero-card { padding:26px; } .scan-box { border-radius:26px; flex-direction:column; } button { width:100%; } .score-grid { grid-template-columns:1fr; } }
  </style>
</head>
<body>
  <main class="radar-shell">
    <nav class="nav">
      <div class="brand"><div class="logo">⌁</div><span>Dyanto AlphaRadar</span></div>
      <div class="status-pill"><span class="dot"></span> Dry-run intelligence mode</div>
    </nav>

    <section class="hero">
      <div class="hero-card">
        <div class="eyebrow">Autonomous Crypto Intelligence</div>
        <h1>Find alpha early. Avoid bad liquidity.</h1>
        <p class="lead">Blue-white market radar for Solana memecoins and DEX opportunities. Scan live pairs, score opportunity, flag risk, and generate analyst-style reports.</p>
        <div class="scan-box">
          <input id="target" value="So11111111111111111111111111111111111111112" placeholder="Paste token address, pair, symbol, or keyword" />
          <button onclick="scan()">Scan Radar</button>
        </div>
        <div class="quick-row">
          <span class="chip" onclick="setTarget('So11111111111111111111111111111111111111112')">SOL demo</span>
          <span class="chip" onclick="setTarget('BONK')">BONK search</span>
          <span class="chip" onclick="setTarget('WIF')">WIF search</span>
        </div>
      </div>
      <div class="visual-card">
        <div class="radar-orb"><div class="sweep"></div></div>
        <h2 style="margin:0 0 12px; font-size:34px; letter-spacing:-.05em; position:relative;">Live DEX Signal Engine</h2>
        <p style="opacity:.86; line-height:1.6; position:relative;">Dexscreener-first collection, GeckoTerminal-ready enrichment, and dry-run analyst reports.</p>
        <div class="visual-stats">
          <div class="mini"><b>DEX</b><span>live pairs</span></div>
          <div class="mini"><b>Risk</b><span>flags</span></div>
          <div class="mini"><b>Report</b><span>markdown</span></div>
        </div>
      </div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <h2>Radar Output</h2>
        <div id="verdict" class="verdict-pill">Waiting for scan</div>
      </div>
      <div class="score-grid">
        <div class="metric-card opportunity"><span>Opportunity</span><strong id="opportunity">—</strong></div>
        <div class="metric-card risk"><span>Risk</span><strong id="risk">—</strong></div>
        <div class="metric-card"><span>Liquidity</span><strong id="liquidity">—</strong></div>
        <div class="metric-card"><span>Volume 24h</span><strong id="volume">—</strong></div>
      </div>
      <div class="gmgn-strip">
        <div class="gmgn-card"><span>Pool Age</span><b id="pool-age">—</b></div>
        <div class="gmgn-card"><span>Vol/Liq</span><b id="vol-liq">—</b></div>
        <div class="gmgn-card"><span>Smart Money</span><b id="smart-money">—</b></div>
        <div class="gmgn-card"><span>Security</span><b id="security-state">—</b></div>
      </div>
      <div class="report-layout">
        <div class="section-card">
          <h3>Token & Market</h3>
          <pre id="market">Click Scan Radar to start.</pre>
        </div>
        <div class="section-card">
          <h3>GMGN-style Security</h3>
          <ul id="security-list"><li>No scan yet.</li></ul>
        </div>
        <div class="section-card">
          <h3>Timeframe Tape</h3>
          <div id="timeframe-grid" class="timeframe-grid"><div class="tf">No scan yet.</div></div>
        </div>
        <div class="section-card">
          <h3>Holder / Wallet Snapshot</h3>
          <pre id="holder-snapshot">Pending scan.</pre>
        </div>
        <div class="section-card">
          <h3>Narrative</h3>
          <ul id="narrative-list"><li>No scan yet.</li></ul>
        </div>
        <div class="section-card">
          <h3>Suggested Actions</h3>
          <ul id="actions-list"><li>No scan yet.</li></ul>
        </div>
      </div>
    </section>
    <div class="footer">Dyanto AlphaRadar · dry-run only · not live trading execution</div>
  </main>
<script>
function money(value){
  value = Number(value || 0);
  if(value >= 1000000) return '$' + (value/1000000).toFixed(2) + 'M';
  if(value >= 1000) return '$' + (value/1000).toFixed(1) + 'K';
  return '$' + value.toFixed(value < 1 ? 4 : 2);
}
function list(el, rows){
  const node = document.getElementById(el);
  node.innerHTML = '';
  (rows && rows.length ? rows : ['No data']).forEach(item => {
    const li = document.createElement('li'); li.textContent = item; node.appendChild(li);
  });
}
function setTarget(value){ document.getElementById('target').value = value; scan(); }
function renderTimeframes(timeframes){
  const node = document.getElementById('timeframe-grid');
  node.innerHTML = '';
  ['m5','h1','h6','h24'].forEach(key => {
    const tf = (timeframes || {})[key] || {};
    const div = document.createElement('div');
    div.className = 'tf';
    div.innerHTML = `<b>${key.toUpperCase()}</b><br>${Number(tf.price_change_pct || 0).toFixed(2)}%<br>${money(tf.volume_usd || 0)}`;
    node.appendChild(div);
  });
}
function renderAnalysis(data){
  if(data.error){ document.getElementById('market').textContent = data.error; return; }
  const score = data.score || {}, market = data.market || {}, id = data.identity || {}, pair = data.primary_pair || {}, details = data.details || {};
  const security = details.security || {}, pool = details.pool || {}, smart = details.smart_money || {}, holder = details.holder_snapshot || {};
  document.getElementById('verdict').textContent = (score.label || 'MONITOR') + ' · ' + (data.verdict || 'Monitor');
  document.getElementById('opportunity').textContent = (score.opportunity_score ?? '—') + '/100';
  document.getElementById('risk').textContent = (score.risk_score ?? '—') + '/100';
  document.getElementById('liquidity').textContent = money(market.liquidity_usd);
  document.getElementById('volume').textContent = money(market.volume_24h);
  document.getElementById('pool-age').textContent = pool.pair_age || '—';
  document.getElementById('vol-liq').textContent = (pool.volume_liquidity_ratio ?? score.vol_liq ?? '—') + 'x';
  document.getElementById('smart-money').textContent = smart.signal || 'pending';
  document.getElementById('security-state').textContent = `${security.liquidity_status || 'unknown'} / ${security.sell_pressure || 'unknown'}`;
  document.getElementById('market').textContent = `${id.name || 'Unknown'} (${id.symbol || 'UNKNOWN'})\nChain: ${id.chain || '-'}\nDEX: ${pair.dex || '-'}\nPrice: ${money(market.price_usd)}\nFDV: ${money(market.fdv)}\nBuys/Sells 24h: ${market.txns_24h_buys || 0} / ${market.txns_24h_sells || 0}\nPair count: ${data.pair_count || 0}\nPair: ${pair.url || '-'}`;
  document.getElementById('holder-snapshot').textContent = `Top holders: ${holder.top_holders || 'pending'}\nDev wallet: ${holder.dev_wallet || 'pending'}\nLP/pool authority: ${holder.lp_pool_authority || 'pending'}\nConcentration: ${holder.concentration_risk || 'unresolved'}\nSmart money: ${smart.interpretation || 'pending enrichment'}`;
  list('security-list', security.flags || score.flags);
  renderTimeframes(details.timeframes);
  list('narrative-list', data.narrative);
  list('actions-list', data.actions);
}
async function scan(){
  const target = document.getElementById('target').value.trim();
  if(!target) return;
  document.getElementById('verdict').innerHTML = '<span class="loading">Scanning live DEX data…</span>';
  const res = await fetch('/api/scan?target=' + encodeURIComponent(target));
  const data = await res.json();
  renderAnalysis(data);
}
</script>
</body>
</html>
"""
