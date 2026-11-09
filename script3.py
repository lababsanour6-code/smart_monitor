import json
import os
import subprocess
import time
import psutil
from datetime import datetime
ROOT_PATH = os.path.abspath(os.sep)
os.environ ["QT_API"] = "pyqt6"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"]= "--remote-allow-origins=*"
import webview
import urllib.request
import urllib.error
from google import genai
client = genai.Client(api_key= os.environ["GEMINI_API_KEY"]) if os.environ.get("GEMINI_API_KEY") else None
import threading
HOST, PORT = "127.0.0.1", 8767
AI_SERVER_URL = "https://smart-monitor-wd40.onrender.com/v1/chat"
ROOT_PATH=os.path.abspath(os.sep)
PAGE = r'''<title>System Monitor Dashboard</title>
<meta name="claude:viewport-fit-sides t_result()
<content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
<style>
/* Layout: top bar, slim icon rail, borderless two-series area chart, then two rows of four cards (sparklines, then bars and rings). Single committed dark look. */
:root {
  --bg: #15142b; --bar: #1b1a33; --card: #211f3b; --well: #14132a; --track: #34325a; --line: #2b2950;
  --fg: #f4f3fc; --muted: #8e8cb0;
  --pink: #f08fcb; --violet: #9a8cf0; --blue: #5aa0f0; --cyan: #62d6e8; --teal: #6ee7c8;
  --good: #4ade80; --warn: #fbbf24; --crit: #f87171;
  --sans: "Manrope", "Segoe UI", system-ui, sans-serif;
  color-scheme: dark;
}
* { box-sizing: border-box; }
html, body { min-height: 100%; }
body {
  margin: 0; background: var(--bg); color: var(--fg); font: 13px/1.45 var(--sans); font-variant-numeric: tabular-nums;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 14px;
}
.shell { max-width: 1500px; margin: 0 auto; display: flex; flex-direction: column; gap: 14px; }
.top { display: flex; align-items: center; gap: 16px; background: var(--bar); border-radius: 12px; padding: 10px 16px; position: relative; z-index: 5; }
.logo { display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 12px; letter-spacing: .05em; text-transform: uppercase; white-space: nowrap; }
.logo i { width: 28px; height: 28px; border-radius: 50%; background: var(--fg); display: grid; place-items: center; flex: none; }
.logo svg { width: 16px; height: 16px; stroke: var(--bg); fill: none; stroke-width: 2.6; stroke-linecap: round; stroke-linejoin: round; }
.searchbox { position: relative; flex: 1 1 200px; min-width: 0; max-width: 760px; margin: 0 auto 0 10px; }
.search { display: flex; align-items: center; gap: 10px; background: var(--well); border-radius: 9px; padding: 0 14px; height: 38px; }
.search svg { width: 15px; height: 15px; stroke: var(--fg); fill: none; stroke-width: 2; flex: none; }
.search input { flex: 1; min-width: 0; background: none; border: 0; outline: 0; color: var(--fg); font: inherit; }
.search input::placeholder { color: var(--muted); }
.search:focus-within { box-shadow: 0 0 0 1px var(--violet); }
.results { position: absolute; left: 0; right: 0; top: 44px; background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 6px; display: none; }
.results.open { display: block; }
.results div { display: grid; grid-template-columns: minmax(0, 1fr) auto auto; gap: 14px; padding: 7px 10px; border-radius: 7px; font-weight: 600; }
.results div:hover { background: var(--well); }
.results b { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-weight: 600; }
.results em { font-style: normal; color: var(--muted); }
.results .none { display: block; color: var(--muted); }
.right { display: flex; align-items: center; gap: 12px; }
.chip { display: flex; align-items: center; gap: 8px; font-size: 11px; font-weight: 700; color: var(--muted); white-space: nowrap; }
.chip .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--warn); }
.chip.live .dot { background: var(--good); animation: pulse 1.6s ease-in-out infinite; }
@keyframes pulse { 50% { opacity: .35; } }
.avatar { width: 34px; height: 34px; border-radius: 50%; background: linear-gradient(135deg, var(--pink), var(--violet)); display: grid; place-items: center; font-weight: 800; font-size: 12px; color: #1b1a33; }
.sq { position: relative; width: 34px; height: 34px; border-radius: 9px; border: 0; background: var(--card); color: var(--fg); display: grid; place-items: center; cursor: pointer; }
.sq svg, .ic svg { width: 17px; height: 17px; stroke: currentColor; fill: none; stroke-width: 1.9; stroke-linecap: round; stroke-linejoin: round; }
.sq .badge { position: absolute; top: 5px; right: 6px; width: 8px; height: 8px; border-radius: 50%; background: var(--crit); display: none; }
.sq.alert .badge { display: block; }
button:focus-visible, a:focus-visible, select:focus-visible { outline: 2px solid var(--violet); outline-offset: 2px; }
.body { display: grid; grid-template-columns: 46px minmax(0, 1fr); gap: 18px; }
.rail { display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 6px 0; border-right: 1px solid var(--line); padding-right: 12px; }
.rail .ic { width: 32px; height: 32px; display: grid; place-items: center; border-radius: 9px; color: var(--muted); background: none; border: 0; cursor: pointer; text-decoration: none; }
.rail .ic:hover, .rail .ic[aria-current="true"] { color: var(--fg); background: var(--card); }
.rail .bottom { margin-top: auto; }
.content { min-width: 0; display: flex; flex-direction: column; gap: 18px; }
.head { display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; flex-wrap: wrap; }
.legend { display: flex; gap: 18px; font-size: 11px; font-weight: 700; padding-top: 4px; }
.legend span::before { content: ""; display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 7px; background: var(--c); }
.range { position: relative; width: 210px; background: var(--card); border-radius: 9px; padding: 7px 14px; }
.range small { display: block; font-size: 10px; color: var(--muted); font-weight: 600; }
.range select { appearance: none; background: none; border: 0; color: var(--fg); font: inherit; font-weight: 600; width: 100%; padding: 0 20px 0 0; cursor: pointer; }
.range select option { background: var(--card); }
.range::after { content: ""; position: absolute; right: 14px; top: 50%; width: 6px; height: 6px; margin-top: -5px; border-right: 2px solid var(--fg); border-bottom: 2px solid var(--fg); transform: rotate(45deg); pointer-events: none; }
canvas { display: block; width: 100%; }
#c-main { height: 320px; }
.row { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }
.card { background: var(--card); border-radius: 12px; padding: 16px 18px; min-width: 0; min-height: 176px; display: flex; flex-direction: column; }
.mh { display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; }
.ttl { font-size: 13px; font-weight: 500; color: var(--fg); margin: 0; }
.val { display: flex; align-items: center; gap: 9px; margin-top: 2px; flex-wrap: wrap; }
.big { font-size: 23px; font-weight: 800; letter-spacing: -.01em; margin: 0; }
.pill { font-size: 10px; font-weight: 700; color: var(--fg); border: 1px solid var(--c); border-radius: 5px; padding: 0 6px; white-space: nowrap; line-height: 17px; }
.dots { width: 28px; height: 28px; border-radius: 50%; background: var(--well); border: 0; color: var(--fg); display: grid; place-items: center; cursor: pointer; flex: none; }
.dots svg { width: 14px; height: 14px; fill: currentColor; }
.spark { height: 84px; margin: auto -6px -4px; width: calc(100% + 12px); }
.bars { flex: 1; display: flex; justify-content: space-between; align-items: stretch; gap: 8px; margin-top: 14px; min-height: 92px; padding: 0 6px; }
.bar { flex: 1; max-width: 16px; display: flex; flex-direction: column; align-items: center; gap: 6px; }
.bar div { flex: 1; width: 6px; background: var(--track); border-radius: 3px; display: flex; align-items: flex-end; overflow: hidden; }
.bar i { display: block; width: 100%; border-radius: 3px; background: var(--c); transition: height .5s, background .3s; }
.bar span { font-size: 10px; font-weight: 600; color: var(--muted); }
.ringrow { flex: 1; display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-top: 4px; }
.key { display: flex; flex-direction: column; gap: 7px; font-size: 11px; font-weight: 600; min-width: 0; }
.key span { display: flex; align-items: center; gap: 8px; white-space: nowrap; }
.key span::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--c); flex: none; }
.ring { width: 104px; height: 104px; flex: none; }
.rt, .rv { fill: none; }
.rt { stroke: var(--track); }
.rv { stroke: var(--c); stroke-linecap: round; transform: rotate(-90deg); transform-origin: 60px 60px; transition: stroke-dasharray .6s cubic-bezier(.2, .8, .2, 1); }
.pop { position: absolute; z-index: 20; background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 10px 14px; font-size: 12px; font-weight: 600; min-width: 190px; box-shadow: 0 8px 24px #0008; }
.pop h4 { margin: 0 0 6px; font-size: 12px; color: var(--muted); font-weight: 700; }
.pop p { margin: 2px 0; display: flex; justify-content: space-between; gap: 18px; }
.pop p span:first-child { color: var(--muted); }
/* Small AI chat window, using the existing dashboard colors */
.ai-overlay { position:fixed; inset:0; z-index:100; display:none; align-items:center; justify-content:center; padding:16px; background:#080817aa; }
.ai-overlay.open { display:flex; }
.ai-window { width:min(540px,96vw); height:min(650px,88vh); display:flex; flex-direction:column; overflow:hidden; background:var(--bar); border:1px solid var(--line); border-radius:13px; box-shadow:0 16px 55px #0009; }
.ai-head { display:flex; justify-content:space-between; align-items:center; padding:13px 16px; border-bottom:1px solid var(--line); }
.ai-head small { display:block; color:var(--muted); margin-top:3px; }
.ai-close { border:0; border-radius:8px; background:var(--card); color:var(--fg); width:32px; height:32px; cursor:pointer; font-size:18px; }
.ai-messages { flex:1; overflow:auto; display:flex; flex-direction:column; gap:10px; padding:14px; }
.ai-msg { max-width:88%; padding:10px 12px; border-radius:10px; white-space:pre-wrap; overflow-wrap:anywhere; line-height:1.5; }
.ai-msg.user { align-self:flex-end; background:#39345f; }
.ai-msg.assistant { align-self:flex-start; background:var(--card); border:1px solid var(--line); }
.ai-msg.error { color:#fecaca; background:#451a1a; border:1px solid #7f1d1d; }
.ai-compose { display:flex; gap:8px; padding:12px; border-top:1px solid var(--line); }
.ai-compose textarea { flex:1; resize:vertical; min-height:42px; max-height:100px; border:1px solid var(--line); border-radius:8px; background:var(--well); color:var(--fg); padding:10px; font:inherit; }
.ai-compose button { border:0; border-radius:8px; padding:0 14px; background:var(--violet); color:#17142b; font-weight:800; cursor:pointer; }
.ai-compose button:disabled { opacity:.5; }
[hidden] { display: none !important; }
@media (max-width: 1100px) { .row { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 760px) {
  .body { grid-template-columns: minmax(0, 1fr); }
  .rail { display: none; }
  .row { grid-template-columns: minmax(0, 1fr); }
  #c-main { height: 230px; }
  .logo span, .chip span:last-child { display: none; }
  .range { width: 100%; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
</style>

<div class="shell">
  <header class="top">
    <div class="logo"><i><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12h4l3-7 4 14 3-7h4"/></svg></i><span>System Monitor</span></div>
    <div class="searchbox">
      <label class="search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg><input id="q" type="search" placeholder="Search processes" aria-label="Search processes" autocomplete="off"></label>
      <div class="results" id="results" role="listbox"></div>
    </div>
    <div class="right">
      <span class="chip" id="mode"><span class="dot"></span><span>Connecting</span></span>
      <button class="sq" id="ai-open" type="button" title="AI Assistant" aria-label="Open AI Assistant">✦</button>
      <button class="sq" id="bell" type="button" aria-label="Alerts"><svg viewBox="0 0 24 24"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 8 3 8H3s3-1 3-8"/><path d="M10 20a2 2 0 0 0 4 0"/></svg><span class="badge"></span></button>
      <div class="avatar" id="avatar" title="Host">PC</div>
    </div>
  </header>

  <div class="body">
    <nav class="rail" aria-label="Sections">
      <a class="ic" href="#overview" aria-label="Overview" aria-current="true"><svg viewBox="0 0 24 24"><path d="M21 12A9 9 0 1 1 12 3v9z"/><path d="M15 3.5A9 9 0 0 1 20.5 9H15z"/></svg></a>
      <a class="ic" href="#metrics" aria-label="Metrics"><svg viewBox="0 0 24 24"><rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/></svg></a>
      <a class="ic" href="#storage" aria-label="Storage and load"><svg viewBox="0 0 24 24"><ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6"/></svg></a>
      <button class="ic" id="focus-search" type="button" aria-label="Search processes"><svg viewBox="0 0 24 24"><path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/></svg></button>
      <button class="ic bottom" id="pause" type="button" aria-label="Pause updates"><svg viewBox="0 0 24 24" id="pause-ic"><path d="M9 5v14M15 5v14"/></svg></button>
    </nav>

    <main class="content">
      <section id="overview" aria-label="CPU and memory history">
        <div class="head">
          <div class="legend"><span style="--c:var(--pink)">CPU</span><span style="--c:var(--violet)">RAM</span></div>
          <label class="range"><small>History range</small><select id="range"><option value="60">Last 60 seconds</option><option value="300">Last 5 minutes</option><option value="900">Last 15 minutes</option></select></label>
        </div>
        <canvas id="c-main" role="img" aria-label="CPU and memory usage history"></canvas>
      </section>

      <section class="row" id="metrics" aria-label="Metrics">
        <article class="card"><div class="mh"><div><p class="ttl">CPU</p><div class="val"><p class="big" id="v-cpu">0%</p><span class="pill" id="b-cpu" style="--c:var(--track)">0</span></div></div><button class="dots" type="button" data-k="cpu" aria-label="CPU statistics"><svg viewBox="0 0 24 24"><circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/></svg></button></div><canvas class="spark" id="s-cpu"></canvas></article>
        <article class="card"><div class="mh"><div><p class="ttl">Memory</p><div class="val"><p class="big" id="v-ram">0 GB</p><span class="pill" id="b-ram" style="--c:var(--violet)">0</span></div></div><button class="dots" type="button" data-k="ram" aria-label="Memory statistics"><svg viewBox="0 0 24 24"><circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/></svg></button></div><canvas class="spark" id="s-ram"></canvas></article>
        <article class="card"><div class="mh"><div><p class="ttl">Disk activity</p><div class="val"><p class="big" id="v-io">0 B/s</p><span class="pill" id="b-io" style="--c:var(--pink)">0</span></div></div><button class="dots" type="button" data-k="io" aria-label="Disk activity statistics"><svg viewBox="0 0 24 24"><circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/></svg></button></div><canvas class="spark" id="s-io"></canvas></article>
        <article class="card"><div class="mh"><div><p class="ttl">Network download</p><div class="val"><p class="big" id="v-net">0 B/s</p><span class="pill" id="b-net" style="--c:var(--violet)">0</span></div></div><button class="dots" type="button" data-k="down" aria-label="Network statistics"><svg viewBox="0 0 24 24"><circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/></svg></button></div><canvas class="spark" id="s-net"></canvas></article>
      </section>

      <section class="row" id="storage" aria-label="Cores, storage and load">
        <article class="card"><div class="mh"><div><p class="ttl">Per-core load</p><div class="val"><p class="big" id="v-cores">—</p><span class="pill" id="b-cores" style="--c:var(--violet)">0</span></div></div></div><div class="bars" id="bars-cores" style="--c:var(--violet)"></div></article>
        <article class="card"><p class="ttl">Storage <span id="disk-name" style="color:var(--muted)"></span></p><div class="val"><p class="big" id="v-disk">0 GB</p></div>
          <div class="ringrow"><div class="key"><span style="--c:var(--track)" id="k-free">Free</span><span style="--c:var(--violet)" id="k-used">Used</span></div>
          <svg class="ring" id="r-disk" viewBox="0 0 120 120" aria-hidden="true"><circle class="rt" cx="60" cy="60" r="46" stroke-width="13"/><circle class="rv" cx="60" cy="60" r="46" stroke-width="13" style="--c:var(--violet)"/></svg></div></article>
        <article class="card"><div class="mh"><div><p class="ttl">Disk I/O, last 7 seconds</p><div class="val"><p class="big" id="v-io2">0 B/s</p><span class="pill" id="b-io2" style="--c:var(--pink)">peak</span></div></div></div><div class="bars" id="bars-io" style="--c:var(--pink)"></div></article>
        <article class="card"><p class="ttl">System load</p><div class="val"><p class="big" id="v-procs">—</p></div>
          <div class="ringrow"><div class="key"><span style="--c:var(--violet)" id="k-cpu">CPU</span><span style="--c:var(--blue)" id="k-ram">RAM</span><span style="--c:var(--cyan)" id="k-swap">Swap</span><span style="--c:var(--teal)" id="k-dsk">Disk</span></div>
          <svg class="ring" id="r-sys" viewBox="0 0 120 120" aria-hidden="true">
            <circle class="rt" cx="60" cy="60" r="52" stroke-width="7"/><circle class="rv" cx="60" cy="60" r="52" stroke-width="7" style="--c:var(--violet)"/>
            <circle class="rt" cx="60" cy="60" r="40" stroke-width="7"/><circle class="rv" cx="60" cy="60" r="40" stroke-width="7" style="--c:var(--blue)"/>
            <circle class="rt" cx="60" cy="60" r="28" stroke-width="7"/><circle class="rv" cx="60" cy="60" r="28" stroke-width="7" style="--c:var(--cyan)"/>
            <circle class="rt" cx="60" cy="60" r="16" stroke-width="7"/><circle class="rv" cx="60" cy="60" r="16" stroke-width="7" style="--c:var(--teal)"/></svg></div></article>
      </section>
    </main>
  </div>
</div>
<div class="pop" id="pop" hidden></div>
<div class="ai-overlay" id="ai-overlay" role="dialog" aria-modal="true" aria-label="AI Assistant">
  <section class="ai-window">
    <header class="ai-head">
      <div><strong>AI Assistant</strong><small>Ask about your computer, Linux, hardware, network or errors.</small></div>
      <button class="ai-close" id="ai-close" type="button" aria-label="Close">×</button>
    </header>
    <div class="ai-messages" id="ai-messages" aria-live="polite">
      <div class="ai-msg assistant">Hello! Ask me anything related to your computer.</div>
    </div>
    <form class="ai-compose" id="ai-form">
      <textarea id="ai-input" rows="2" placeholder="Write your question..." aria-label="Your question"></textarea>
      <button id="ai-send" type="submit">Send</button>
    </form>
  </section>
</div>

<script>
const MAXH = 900, GB = 2 ** 30;
const col = { pink: "#f08fcb", violet: "#9a8cf0", blue: "#5aa0f0", cyan: "#62d6e8", muted: "#8e8cb0" };
const $ = (s) => document.querySelector(s);
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const walk = (v, step, a, b) => clamp(v + (Math.random() - 0.5) * step, a, b);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

function bytes(n) { const u = ["B", "KB", "MB", "GB", "TB"]; let i = 0; while (n >= 1024 && i < 4) { n /= 1024; i++; } return (i ? n.toFixed(i > 2 ? 1 : 0) : Math.round(n)) + " " + u[i]; }
const rate = (n) => bytes(n) + "/s";
const pct = (v) => Math.round(v) + "%";
function niceMax(v) { v = Math.max(v, 1024); const mag = 10 ** Math.floor(Math.log10(v)); for (const m of [1, 2, 5, 10]) if (v <= m * mag) return m * mag; return 10 * mag; }
function level(v, base) { return v >= 90 ? "var(--crit)" : v >= 75 ? "var(--warn)" : base; }
const avg = (a, n, skip = 0) => { const s = a.slice(Math.max(0, a.length - n - skip), a.length - skip); return s.reduce((x, y) => x + y, 0) / (s.length || 1); };

const hist = { cpu: [], ram: [], io: [], down: [], up: [] };
let range = 60, last = null, paused = false;

function draw(cv, series, colors, o) {
  const dpr = window.devicePixelRatio || 1, w = cv.clientWidth, h = cv.clientHeight;
  if (!w || !h) return;
  if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); }
  const c = cv.getContext("2d");
  c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, w, h);
  const ax = !!o.axes, L = ax ? 42 : 0, R = ax ? 4 : 0, T = ax ? 10 : 8, B = ax ? 30 : 4;
  const pw = w - L - R, ph = h - T - B, N = o.N;
  const vis = series.map((s) => s.slice(-N));
  const vmax = o.max || niceMax(Math.max(1, ...vis.flat()) * 1.15);
  if (ax) {
    c.font = "600 11px Manrope, sans-serif"; c.fillStyle = col.muted; c.textBaseline = "middle"; c.textAlign = "left";
    for (let i = 0; i <= 5; i++) c.fillText(o.fmtY(vmax * (5 - i) / 5), 0, T + ph * i / 5);
    c.textBaseline = "alphabetic";
    const n = w > 560 ? 7 : 4;
    for (let i = 0; i < n; i++) {
      const sec = Math.round(N * (1 - i / (n - 1)));
      const t = sec === 0 ? "now" : N >= 300 ? "-" + Math.round(sec / 60) + "m" : "-" + sec + "s";
      c.textAlign = i === 0 ? "left" : i === n - 1 ? "right" : "center";
      c.fillText(t, L + pw * i / (n - 1), h - 6);
    }
  }
  vis.forEach((s, k) => {
    if (s.length < 2) return;
    const off = N - s.length;
    const pts = s.map((v, i) => [L + (off + i) * pw / (N - 1), T + ph - Math.min(v, vmax) / vmax * ph]);
    const line = new Path2D(); line.moveTo(pts[0][0], pts[0][1]);
    for (let i = 1; i < pts.length; i++) { const cx = (pts[i - 1][0] + pts[i][0]) / 2; line.bezierCurveTo(cx, pts[i - 1][1], cx, pts[i][1], pts[i][0], pts[i][1]); }
    if (o.fill) {
      const f = new Path2D(line); f.lineTo(pts[pts.length - 1][0], T + ph); f.lineTo(pts[0][0], T + ph); f.closePath();
      const g = c.createLinearGradient(0, T, 0, T + ph); g.addColorStop(0, colors[k] + (o.big ? "88" : "66")); g.addColorStop(1, colors[k] + "00");
      c.fillStyle = g; c.fill(f);
    }
    c.strokeStyle = colors[k]; c.lineWidth = o.big ? 1.6 : 1.8; c.lineJoin = "round"; c.stroke(line);
  });
}

function redraw() {
  draw($("#c-main"), [hist.cpu, hist.ram], [col.pink, col.violet], { N: range, max: 100, axes: true, fmtY: pct, fill: true, big: true });
  draw($("#s-cpu"), [hist.cpu], [col.pink], { N: 60, max: 100 });
  draw($("#s-ram"), [hist.ram], [col.blue], { N: 60, max: 100, fill: true });
  draw($("#s-io"), [hist.io], [col.pink], { N: 60, fill: true });
  draw($("#s-net"), [hist.down], [col.violet], { N: 60 });
}

function ring(svg, idx, p) {
  const circles = $(svg).querySelectorAll(".rv"), el = circles[idx], r = +el.getAttribute("r"), C = 2 * Math.PI * r;
  el.setAttribute("stroke-dasharray", (C * Math.max(p, 0.5) / 100) + " " + C);
}
function bars(sel, values, labels, max) {
  const box = $(sel);
  if (box.children.length !== values.length) box.innerHTML = values.map((_, i) => `<div class="bar"><div><i style="height:0%"></i></div><span>${labels[i]}</span></div>`).join("");
  values.forEach((v, i) => { const e = box.children[i].querySelector("i"); e.style.height = clamp(v / max * 100, 3, 100) + "%"; });
}
function delta(el, d, f) { el.textContent = f(Math.abs(d)) + " " + (d >= 0 ? "↗" : "↘"); }

function pushHist(d) {
  for (const [k, v] of [["cpu", d.cpu], ["ram", d.ram.percent], ["io", d.disk.read + d.disk.write], ["down", d.net.down], ["up", d.net.up]]) { hist[k].push(v); if (hist[k].length > MAXH) hist[k].shift(); }
}

function render(d) {
  last = d;
  pushHist(d);
  $("#v-cpu").textContent = d.cpu.toFixed(1) + "%"; delta($("#b-cpu"), avg(hist.cpu, 5) - avg(hist.cpu, 5, 5), (x) => x.toFixed(1));
  $("#v-ram").textContent = bytes(d.ram.used); delta($("#b-ram"), avg(hist.ram, 5) - avg(hist.ram, 5, 5), (x) => x.toFixed(2));
  const io = d.disk.read + d.disk.write;
  $("#v-io").textContent = rate(io); delta($("#b-io"), avg(hist.io, 5) - avg(hist.io, 5, 5), bytes);
  $("#v-net").textContent = rate(d.net.down); delta($("#b-net"), avg(hist.down, 5) - avg(hist.down, 5, 5), bytes);

  const g = Math.ceil(d.cores.length / 16), cores = [];
  for (let i = 0; i < d.cores.length; i += g) { const s = d.cores.slice(i, i + g); cores.push(s.reduce((a, b) => a + b, 0) / s.length); }
  bars("#bars-cores", cores, cores.map((_, i) => i * g), 100);
  $("#v-cores").textContent = d.cores.length + " cores"; delta($("#b-cores"), avg(hist.cpu, 5) - avg(hist.cpu, 5, 5), (x) => x.toFixed(1));

  $("#disk-name").textContent = d.disk.name; $("#v-disk").textContent = bytes(d.disk.used);
  $("#k-free").textContent = bytes(d.disk.total - d.disk.used) + " Free"; $("#k-used").textContent = bytes(d.disk.used) + " Used";
  ring("#r-disk", 0, d.disk.percent);

  const last7 = hist.io.slice(-7), peak = Math.max(...last7, 1);
  bars("#bars-io", last7, last7.map((_, i) => i === 6 ? "0" : "-" + (6 - i)), niceMax(peak));
  $("#v-io2").textContent = rate(io); $("#b-io2").textContent = "peak " + bytes(peak);

  $("#v-procs").textContent = d.nproc + " tasks";
  $("#k-cpu").textContent = pct(d.cpu) + " CPU"; $("#k-ram").textContent = pct(d.ram.percent) + " RAM"; $("#k-swap").textContent = pct(d.swap) + " Swap"; $("#k-dsk").textContent = pct(d.disk.percent) + " Disk";
  ring("#r-sys", 0, d.cpu); ring("#r-sys", 1, d.ram.percent); ring("#r-sys", 2, d.swap); ring("#r-sys", 3, d.disk.percent);

  $("#bell").classList.toggle("alert", alerts(d).length > 0);
  if (d.host) $("#avatar").textContent = d.host.slice(0, 2).toUpperCase();
  renderResults();
  redraw();
}

function alerts(d) {
  const a = [];
  if (d.cpu > 85) a.push(["CPU", pct(d.cpu)]);
  if (d.ram.percent > 85) a.push(["Memory", pct(d.ram.percent)]);
  if (d.disk.percent > 90) a.push(["Disk " + d.disk.name, pct(d.disk.percent)]);
  return a;
}

function renderResults() {
  const box = $("#results"), v = $("#q").value.trim().toLowerCase();
  if (!last || !v) { box.classList.remove("open"); return; }
  const rows = last.procs.filter((p) => p.name.toLowerCase().includes(v)).slice(0, 8);
  box.innerHTML = rows.length ? rows.map((p) => `<div role="option"><b>${esc(p.name)}</b><em>${p.cpu.toFixed(1)}% CPU</em><em>${bytes(p.rss)}</em></div>`).join("") : `<div class="none">No process matches "${esc($("#q").value.trim())}".</div>`;
  box.classList.add("open");
}

const pop = $("#pop");
function openPop(btn, html) {
  pop.innerHTML = html; pop.hidden = false;
  const r = btn.getBoundingClientRect(), w = pop.offsetWidth;
  pop.style.left = Math.max(8, Math.min(r.right + window.scrollX - w, window.scrollX + document.documentElement.clientWidth - w - 8)) + "px";
  pop.style.top = (r.bottom + window.scrollY + 8) + "px";
}
document.querySelectorAll(".dots").forEach((b) => b.addEventListener("click", (e) => {
  e.stopPropagation();
  const k = b.dataset.k, a = hist[k].slice(-range), isPct = k === "cpu" || k === "ram", f = isPct ? (x) => x.toFixed(1) + "%" : rate;
  if (!a.length) return;
  openPop(b, `<h4>${b.getAttribute("aria-label")} · ${range >= 300 ? range / 60 + " min" : range + " s"}</h4><p><span>Minimum</span><span>${f(Math.min(...a))}</span></p><p><span>Average</span><span>${f(avg(a, a.length))}</span></p><p><span>Maximum</span><span>${f(Math.max(...a))}</span></p>`);
}));
$("#bell").addEventListener("click", (e) => {
  e.stopPropagation();
  const a = last ? alerts(last) : [];
  openPop($("#bell"), `<h4>Alerts</h4>` + (a.length ? a.map(([n, v]) => `<p><span>${esc(n)}</span><span style="color:var(--crit)">${v}</span></p>`).join("") : `<p><span>No active alerts.</span></p>`));
});
document.addEventListener("click", (e) => { if (!pop.contains(e.target)) pop.hidden = true; if (!$(".searchbox").contains(e.target)) $("#results").classList.remove("open"); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape") { pop.hidden = true; $("#results").classList.remove("open"); } });

let mode = "probe", simState = null;
function setMode(m) {
  mode = m;
  const chip = $("#mode");
  chip.classList.toggle("live", m === "live");
  chip.lastElementChild.textContent = m === "live" ? "Live · real data" : "Connection lost";
}
async function fetchStats() {
  try {
    const r = await fetch("/api/stats", { cache: "no-store" });
    if (!r.ok) throw new Error("HTTP " + r.status);
    const d = await r.json();
    if (typeof d.cpu !== "number" || !d.ram || !d.disk || !d.net) throw new Error("Invalid data from Python");
    if (mode !== "live") setMode("live");
    return d;
  } catch (e) {
    if (mode !== "lost") setMode("lost");
    console.error("Could not get real system data:", e);
    return null;
  }
}

const SIM_PROCS = [["chrome.exe", 9, 1.9e9], ["code.exe", 6, 1.2e9], ["python.exe", 14, 4.2e8], ["node.exe", 5, 3.6e8], ["Teams.exe", 4, 9.1e8], ["firefox.exe", 3, 7.4e8], ["docker.exe", 3, 6e8], ["explorer.exe", 1.5, 2.2e8], ["spotify.exe", 1.2, 3.1e8], ["slack.exe", 1.5, 4.4e8]];
function simStats() {
  if (!simState) simState = { cpu: 34, ram: 66, cores: Array.from({ length: 8 }, () => 15 + Math.random() * 35), down: 1.2e6, io: 2e6, up: 3e5, procs: SIM_PROCS.map(([name, base, rss], i) => ({ name, base, rss, pid: 1000 + i * 733, cpu: base })) };
  const s = simState;
  s.cpu = walk(s.cpu, 16, 10, 92); s.ram = walk(s.ram, 5, 50, 84);
  s.cores = s.cores.map((v) => walk(v * .6 + s.cpu * .4, 34, 2, 100));
  s.down = Math.abs(walk(s.down, 3e6, 0, 9e6)); s.up = Math.abs(walk(s.up, 8e5, 0, 2.5e6)); s.io = Math.abs(walk(s.io, 4e6, 0, 9e6));
  s.procs.forEach((p) => { p.cpu = Math.max(.1, walk(p.cpu, p.base * 1.2, 0, p.base * 3)); });
  const procs = [...s.procs].sort((a, b) => b.cpu - a.cpu).map((p) => ({ name: p.name, pid: p.pid, cpu: p.cpu, rss: p.rss }));
  const total = 16 * GB;
  return { cpu: s.cpu, cores: s.cores, ram: { percent: s.ram, used: total * s.ram / 100, total }, swap: s.ram / 6,
    disk: { name: "C:\\", percent: 62, used: 310 * GB, total: 500 * GB, read: s.io * .6, write: s.io * .4 },
    net: { down: s.down, up: s.up }, uptime: 3 * 86400, nproc: 214, procs, host: "PC" };
}

// AI chat window: sends questions to the existing Python server.
const aiOverlay = $("#ai-overlay"), aiMessages = $("#ai-messages"), aiInput = $("#ai-input");
const aiHistory = [];
function addAiMessage(role, content, isError=false) {
  const item = document.createElement("div");
  item.className = "ai-msg " + role + (isError ? " error" : "");
  item.textContent = content;
  aiMessages.appendChild(item);
  aiMessages.scrollTop = aiMessages.scrollHeight;
}
$("#ai-open").addEventListener("click", () => { aiOverlay.classList.add("open"); aiInput.focus(); });
$("#ai-close").addEventListener("click", () => aiOverlay.classList.remove("open"));
aiOverlay.addEventListener("click", (e) => { if (e.target === aiOverlay) aiOverlay.classList.remove("open"); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape") aiOverlay.classList.remove("open"); });
$("#ai-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = aiInput.value.trim();
  if (!question) return;
  aiInput.value = "";
  addAiMessage("user", question);
  aiHistory.push({role:"user", content:question});
  const send = $("#ai-send");
  send.disabled = true; send.textContent = "...";
  try {
    const response = await fetch("/api/chat", {
      method:"POST", headers:{"Content-Type":"application/json"},
      body:JSON.stringify({messages:aiHistory.slice(-16)})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || ("HTTP " + response.status));
    addAiMessage("assistant", data.reply);
    aiHistory.push({role:"assistant", content:data.reply});
  } catch (err) {
    addAiMessage("assistant", "AI error: " + err.message, true);
    aiHistory.pop();
  } finally {
    send.disabled = false; send.textContent = "Send"; aiInput.focus();
  }
});

async function monitorLoop() {
  while (true) {
    if (!paused) {
      const d = await fetchStats();
      if (d) render(d);
    }
    await sleep(1000);
  }
}

$("#range").addEventListener("change", (e) => { range = +e.target.value; redraw(); });
$("#q").addEventListener("input", renderResults);
$("#q").addEventListener("focus", renderResults);
$("#focus-search").addEventListener("click", () => $("#q").focus());
$("#pause").addEventListener("click", () => {
  paused = !paused;
  $("#pause-ic").innerHTML = paused ? '<path d="M7 4l13 8-13 8z"/>' : '<path d="M9 5v14M15 5v14"/>';
  $("#pause").setAttribute("aria-label", paused ? "Resume updates" : "Pause updates");
  const chip = $("#mode"); if (paused) { chip.classList.remove("live"); chip.lastElementChild.textContent = "Paused"; } else setMode(mode);
});
document.querySelectorAll('.rail a').forEach((a) => a.addEventListener("click", () => { document.querySelectorAll(".rail a").forEach((x) => x.removeAttribute("aria-current")); a.setAttribute("aria-current", "true"); }));
window.addEventListener("resize", redraw);
monitorLoop();
</script>
'''
def log_message(self, *args):
    pass
import socket
import ipaddress
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

def safe_run(cmd, **kw):
    try:
        return subprocess.run(cmd, **kw)
    except Exception as e:
        print("command failed:", cmd[0], "->", e)
        return subprocess.CompletedProcess(cmd, 1, "", "")

_prev = {"disk": None, "net": None, "t": None}
def collect_stats():
    now = time.time()
    dio, nio = psutil.disk_io_counters(), psutil.net_io_counters()
    read = write = down = up = 0
    if _prev["t"] :
        dt = max(now - _prev["t"], 0.001)
    if dio and _prev["disk"]:
        read = (dio.read_bytes - _prev["disk"].read_bytes) / dt
        write = (dio.write_bytes - _prev["disk"].write_bytes) / dt
        down = (nio.bytes_recv - _prev["net"].bytes_recv) / dt
        up = (nio.bytes_sent - _prev["net"].bytes_sent) / dt
    _prev.update(disk=dio, net=nio, t=now)
    vm, du = psutil.virtual_memory(), psutil.disk_usage(ROOT_PATH)
    procs = []
    for p in psutil.process_iter(["name", "pid", "cpu_percent", "memory_info"]):
        i = p.info
        procs.append({"name": i["name"] or "?", "pid": i["pid"], "cpu": i["cpu_percent"] or 0.0,
                      "rss": i["memory_info"].rss if i["memory_info"] else 0})
    procs.sort(key=lambda x: x["cpu"], reverse=True)
    cores = psutil.cpu_percent(interval=None, percpu=True)
    return {"cpu": sum(cores) / len(cores), "cores": cores,
            "ram": {"percent": vm.percent, "used": vm.used, "total": vm.total},
            "swap": psutil.swap_memory().percent,
            "disk": {"name": ROOT_PATH, "percent": du.percent, "used": du.used, "total": du.total, "read": read, "write": write},
            "net": {"down": down, "up": up}, "uptime": now - psutil.boot_time(),
            "nproc": len(psutil.pids()), "procs": procs, "host": socket.gethostname()}

ACTIVE_MONITOR = None

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 64000:
                raise ValueError("Invalid request size.")
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            messages = payload.get("messages", [])
            if not isinstance(messages, list) or not messages:
                raise ValueError("Please enter a question.")
            if ACTIVE_MONITOR is None:
                raise RuntimeError("The monitor is not ready.")
            reply = ACTIVE_MONITOR.chat_ai(messages)
            body = json.dumps({"reply": reply}).encode("utf-8")
            status_code = 200
        except Exception as exc:
            print("[AI CHAT ERROR]", str(exc), flush=True)
            body = json.dumps({"error": str(exc)}).encode("utf-8")
            status_code = 503
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/api/stats"):
            body, ctype = json.dumps(collect_stats()).encode(), "application/json"
        else:
            body = ("<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>" + PAGE).encode()
            ctype = "text/html; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
def log_message(self, *args):
    pass
def start_server():
    srv = ThreadingHTTPServer((HOST, PORT), Handler)
    threading.Thread(target=srv.serve_forever).start()
class Monitor :
    def __init__(self):
        self.start_time=None
        self.counted=False
        self.second_warning_sent=False
        self.last_cpu = self.last_ram = self.last_disk = 0
        self.last_ai_time = 0
        self.count = 0
        self.ram_count = 0
        self.ram_counted = False
        self.ram_start_time = None
        self.disk_start_time = None
        self.cpu_critical_sent = False
        self.cpu_five_alert_sent = False
        self.ram_five_alert_sent = False
        self.disk_alert_sent = False
        self.blocked_ips = set()

    def _ask_remote_ai(self, messages):
        payload = {
            "messages": messages[-20:],
            "cpu": self.last_cpu,
            "ram": self.last_ram,
            "disk": self.last_disk
        }

        request = urllib.request.Request(
            AI_SERVER_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                result = json.loads(response.read().decode("utf-8"))

            reply = result.get("reply")
            if not reply:
                raise RuntimeError("Gemini returned an empty answer.")

            return reply

        except urllib.error.HTTPError as e:
            raise RuntimeError(
                f"AI server error {e.code}: {e.read().decode('utf-8')}"
            )

        except Exception as e:
            raise RuntimeError(f"AI connection failed: {e}")


    def ask_ai(self, question, cpu, ram, disk):
        self.last_cpu, self.last_ram, self.last_disk = cpu, ram, disk
        return self._ask_remote_ai([
            {"role": "user", "content": str(question)}
        ])


    def chat_ai(self, messages):
        if not isinstance(messages, list) or not messages:
            raise ValueError("Invalid chat messages.")

        return self._ask_remote_ai(messages)

    def chat_loop(self):
        while True:
            q = input("\nAsk the AI about CPU, RAM or Disk (type q to quit): ")
            if q.strip().lower() == "q":
                break
            try:
                print(self.ask_ai(q, self.last_cpu, self.last_ram, self.last_disk))
            except Exception as e:
                print("AI error:", e)
    def send_notification(self, title, message):
        result = safe_run(
            ["notify-send", "-u", "critical", title, message],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print("[NOTIFICATION ERROR]", result.stderr or "notify-send is unavailable")
        return result.returncode == 0
    def block_suspicious_ip(self, ip_address):
        try:
            ipaddress.ip_address(ip_address)
        except ValueError:
            print(f"[!] Invalid IP address: {ip_address}")
            return False

        status = safe_run(["sudo", "-n", "ufw", "status"], capture_output=True, text=True)
        if status.returncode != 0 or "Status: active" not in status.stdout:
            print("[!] UFW is not active or passwordless sudo is unavailable.")
            return False
        command = ["sudo", "-n", "ufw", "deny", "from", ip_address]
        result = safe_run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[+] IP {ip_address} blocked.")
            return True
        print(f"[!] Could not block {ip_address}: {result.stderr or result.stdout}")
        return False
    def update_loop(self,window):
        start_server()
        with open("monitor_gui.html", "w", encoding="utf-8") as f:
            f.write("<!doctype html><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>" + PAGE)
        threading.Thread(target=self.loop, daemon=True).start()
        self.window = webview.create_window("System Monitor", f"http://{HOST}:{PORT}/")
        webview.start()
    def loop(self):
        print("System and Network Monitor in Progress....")
        while True:
            alerts = []
            cpu = psutil.cpu_percent(interval=1)
            print("the user consumes processor power :", cpu)
            result = subprocess.run(["bash","-c","top -bn1 | grep 'cpu(s)'"],capture_output=True,text=True)
            print("System Cpu Data : ", result.stdout)
            if cpu <= 60:
                status= "normal"
                print('normal')
                self.start_time=None
                self.counted = False
                self.cpu_critical_sent=False
                self.first_alert_sent = False
            elif 60 < cpu <=85 :
                status= "warning"
                print('warning')
                self.start_time=None
                self.counted = False
                self.second_warning_sent = False
                self.cpu_critical_sent = False
                self.first_alert_sent = False
            elif cpu > 85:
                status= "so high"
                if self.start_time == None:
                    print('so high ')
                    alerts.append(f"CPU usage is very high ({cpu}%)")
                    self.start_time=time.perf_counter()
                elapsed_time=time.perf_counter()-self.start_time
                if elapsed_time > 60 :
                    if not self.counted :
                        self.count += 1
                        self.counted = True
                        if self.count >= 5 and not self.cpu_five_alert_sent:
                            self.send_notification("Smart Server Monitor",
                                                 "CPU has reached 5 high-usage episodes. Please check the processor.")
                            self.cpu_five_alert_sent = True
                        if elapsed_time >= 180 and not self.cpu_critical_sent:
                            self.send_notification("Smart Server Monitor",
                                                   "CPU usage has remained above 85% for 3 minutes. Please check the processor.")
                            self.cpu_critical_sent = True
                        if not self.second_warning_sent:
                            print('please chek the processor status again')
                            self.second_warning_sent = True
            with open('monitor.log','a') as file :
                file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | CPU : {cpu}% |Status : {status} \n")
            ram = psutil.virtual_memory().percent
            print("the ram usage is :",ram)
            result_ram = subprocess.run(["free", "-m"], capture_output=True, text=True)
            print("System Ram Data : \n ", result_ram.stdout)
            if ram <= 60 :
                status = "normal"
                print('normal')
                self.ram_start_time=None
                self.ram_counted=None
                self.ram_five_alert_sent=False
            elif 60 < ram <=85 :
                status = "warning"
                print('warning')
                self.ram_start_time=None
                self.ram_counted = None
                self.ram_five_alert_sent = False
            elif ram > 85 :
                status = "so high"
                if  not self.ram_start_time :
                    print('so high ')
                    alerts.append(f"RAM usage is very high ({ram}%)")
                    self.ram_start_time=time.perf_counter()
                elpsed_time = time.perf_counter()- self.ram_start_time
                if elpsed_time > 60 and not self.ram_five_alert_sent:
                    self.count+=1
                    self.counted = True
                if self.count >= 5 and not self.ram_five_alert_sent:
                    self.send_notification("Smart Server Monitor",
                                           " RAM has reached 5 high_usage episodes. Please check memory usage.")
                    self.disk_alert_sent = True
            with open('monitor.log', 'a') as file:
                file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | RAM : {ram}% |Status : {status} \n")
            disk = psutil.disk_usage('/')
            print("the disk usage is :",disk.percent)
            result_disk = subprocess.run(["df", "-h" , "/"], capture_output=True, text=True)
            print("System Disk Data : \n ", result_disk.stdout)
            if disk.percent <= 70 :
                status = "normal"
                print('normal')
                self.disk_start_time=None
                self.cpu_alert_sent=None
            elif 70 < disk.percent <=90 :
                status = "warning"
                print('warning')
                self.disk_start_time=None
                self.cpu_alert_sent = None
            elif disk.percent > 90 :
                status = "critical"
                if self.disk_start_time == None:
                    print('critical ')
                    alerts.append(f"Disk is almost full ({disk.percent}%)")
                    self.disk_start_time = time.perf_counter()
                elapsed_time = time.perf_counter() - self.disk_start_time
                if elapsed_time > 300 and not self.disk_alert_sent:
                    self.send_notification("Smart Server Monitor",
                                           "Disk usage has remained above 90% for 5 minutes. Please free some space.")
                    self.disk_alert_sent = True

            with open('monitor.log', 'a') as file:
                file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | DISK : {disk}% |Status : {status}\n")
            with open("monitor_data.json", "w") as jf:
                json.dump({"cpu": float(cpu), "ram": float(ram) , "disk": float(disk.percent) }, jf)
            result = subprocess.run(["bash", "-c", "top -bn1 | grep 'cpu(s)'"], capture_output=True, text=True)
            connections_data = safe_run(["ss", "-tun"], capture_output=True, text=True)
            suspicious_ips = [x.strip() for x in os.environ.get("SUSPICIOUS_IPS", "").split(",") if x.strip()]
            for suspicious_ip in suspicious_ips:
                try:
                    ipaddress.ip_address(suspicious_ip)
                    endpoint_match = any(
                        token == suspicious_ip or token.startswith(suspicious_ip + ":")
                        or token.startswith("[" + suspicious_ip + "]:")
                        for token in connections_data.stdout.split()
                    )
                    if endpoint_match and suspicious_ip not in self.blocked_ips:
                        if self.block_suspicious_ip(suspicious_ip):
                            self.blocked_ips.add(suspicious_ip)
                except ValueError:
                    print(f"[!] Ignoring invalid SUSPICIOUS_IPS entry: {suspicious_ip}")
            self.last_cpu, self.last_ram, self.last_disk = cpu, ram, disk.percent
            if alerts and time.time() - self.last_ai_time > 120:
                self.last_ai_time = time.time()
                question = ("These alerts were triggered: " + "; ".join(alerts) +
                            ". What is the likely cause of each one, and how can I fix it?")
                threading.Thread(
                    target=lambda: print("\n[AI]", self.ask_ai(question, cpu, ram, disk.percent)),
                    daemon=True
                ).start()
            time.sleep(1)
    def search_log(self, keyword):
        with open('monitor.log','r') as file :
            for line in file :
                if keyword in line:
                    print(line.strip())
if __name__ == "__main__":
    monitor=Monitor()
    ACTIVE_MONITOR=monitor
    monitor.update_loop(None)






