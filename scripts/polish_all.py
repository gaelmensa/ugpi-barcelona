"""
Comprehensive polish pass:
  1. Replace hero mockup with faithful, bigger replica of real tool UI
  2. Enlarge satellite orbit decoration
  3. Methodology page: add data-pipeline SVG decoration to hero
  4. Nav dropdown: Methodology → hover reveals Heat / Green Space / Social Vulnerability
  5. Scroll progress bar on validation.html, about.html, methodology.html
"""
import os, re

# ─────────────────────────────────────────────────────────────────────
# 1. HERO MOCKUP — faithful replica, 560×370 px
# ─────────────────────────────────────────────────────────────────────
NEW_MOCKUP_CSS = """
/* ── Hero mockup (faithful replica) ─────────────────────── */
.hero-mockup-card {
  width: 560px; height: 370px;
  background: #f2f4f7;
  border-radius: 12px;
  border: 1px solid rgba(0,0,0,0.12);
  box-shadow: 0 0 100px rgba(126,184,212,0.09), 0 32px 80px rgba(0,0,0,0.65);
  transform: perspective(1100px) rotateX(6deg) rotateY(-14deg) rotateZ(1deg);
  transition: transform 0.55s cubic-bezier(.23,1,.32,1), box-shadow 0.55s;
  overflow: hidden; position: relative; will-change: transform;
  display: flex; flex-direction: column;
}
/* titlebar */
.mockup-titlebar {
  height: 26px; background: #eaecf0; border-bottom: 1px solid rgba(0,0,0,0.07);
  display: flex; align-items: center; padding: 0 10px; gap: 5px; flex-shrink: 0;
}
.mockup-dot { width: 8px; height: 8px; border-radius: 50%; }
.mockup-dot-r { background: #ff5f57; }
.mockup-dot-y { background: #ffbd2e; }
.mockup-dot-g { background: #28ca41; }
.mockup-titlebar-label {
  margin-left: 8px; font-size: 9px; color: rgba(0,0,0,0.30);
  font-family: 'Inter',sans-serif; letter-spacing: 0.06em;
}
/* three-column body */
.mockup-body { display: flex; flex: 1; min-height: 0; }
/* LEFT SIDEBAR */
.mk-left {
  width: 110px; flex-shrink: 0; background: #f2f4f7;
  border-right: 1px solid rgba(0,0,0,0.07);
  padding: 8px 7px; display: flex; flex-direction: column; gap: 4px;
  overflow: hidden;
}
.mk-title  { height: 7px; border-radius: 3px; background: rgba(0,0,0,0.18); width: 90%; margin-bottom: 1px; }
.mk-sub    { height: 5px; border-radius: 2px; background: rgba(0,0,0,0.09); width: 70%; margin-bottom: 5px; }
.mk-search {
  height: 16px; border-radius: 4px;
  background: rgba(0,0,0,0.06); border: 1px solid rgba(0,0,0,0.10);
  margin-bottom: 6px; display: flex; align-items: center; padding: 0 5px; gap: 3px;
}
.mk-search-icon { width: 6px; height: 6px; border-radius: 50%; border: 1px solid rgba(0,0,0,0.20); flex-shrink: 0; }
.mk-search-bar  { flex: 1; height: 3px; border-radius: 2px; background: rgba(0,0,0,0.08); }
.mk-dot-row  { display: flex; align-items: center; gap: 4px; margin-bottom: 2px; }
.mk-dot      { width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0; }
.mk-dotlabel { height: 4px; border-radius: 2px; background: rgba(0,0,0,0.13); flex: 1; }
.mk-sep    { height: 1px; background: rgba(0,0,0,0.07); margin: 5px 0; }
.mk-label  { height: 4px; border-radius: 2px; background: rgba(0,0,0,0.18); width: 55%; margin-bottom: 5px; }
.mk-btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3px; margin-bottom: 5px; }
.mk-btn      { height: 15px; border-radius: 4px; background: #fff; border: 1px solid rgba(0,0,0,0.10); }
.mk-btn.on   { background: #1a2535; border-color: transparent; }
.mk-btn-full { height: 13px; border-radius: 3px; background: rgba(0,0,0,0.04); border: 1px solid rgba(0,0,0,0.08); margin-bottom: 2px; }
.mk-slider-row { display: flex; align-items: center; gap: 3px; margin-bottom: 3px; }
.mk-slider-dot { width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0; }
.mk-slider-track { flex: 1; height: 3px; border-radius: 2px; background: rgba(0,0,0,0.10); position: relative; }
.mk-slider-fill  { position: absolute; left: 0; top: 0; bottom: 0; border-radius: 2px; width: 33%; }
.mk-slider-thumb { position: absolute; top: 50%; width: 6px; height: 6px; border-radius: 50%; background: #fff; border: 1px solid rgba(0,0,0,0.25); transform: translate(-50%,-50%); left: 33%; }
.mk-bottom { display: grid; grid-template-columns: 1fr 1fr; gap: 3px; margin-top: auto; padding-top: 5px; }
.mk-bottom-btn { height: 15px; border-radius: 4px; }
.mk-bottom-btn.export { background: rgba(0,0,0,0.05); border: 1px solid rgba(0,0,0,0.10); }
.mk-bottom-btn.how    { background: #1a2535; }
/* MAP AREA */
.mk-map {
  flex: 1; position: relative; overflow: hidden;
  background: #1a2535;
}
.mk-map-grid {
  display: grid; grid-template-columns: repeat(18,1fr); grid-template-rows: repeat(13,1fr);
  gap: 0.7px; width: 100%; height: 100%;
}
.mk-cell { transition: opacity 0.4s; }
/* Zoom controls */
.mk-zoom {
  position: absolute; top: 7px; left: 7px;
  display: flex; flex-direction: column;
  background: #fff; border-radius: 4px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.3);
  overflow: hidden;
}
.mk-zoom-btn {
  width: 16px; height: 14px; display: flex; align-items: center; justify-content: center;
  font-size: 10px; font-family: 'Inter',sans-serif; font-weight: 700;
  color: #333; line-height: 1; cursor: default;
}
.mk-zoom-btn:first-child { border-bottom: 1px solid rgba(0,0,0,0.10); }
@keyframes mk-scan {
  0%   { left: -15%; }
  100% { left: 115%; }
}
.mk-scan {
  position: absolute; top: 0; bottom: 0; width: 35px;
  background: linear-gradient(90deg,transparent,rgba(126,184,212,0.12),transparent);
  animation: mk-scan 5.5s ease-in-out infinite 1s;
  pointer-events: none;
}
/* Floating chips */
@keyframes mk-chip-a { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-4px)} }
@keyframes mk-chip-b { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-4px)} }
.mk-chip {
  position: absolute; z-index: 5;
  background: rgba(8,20,32,0.92); border: 1px solid rgba(126,184,212,0.40);
  border-radius: 6px; padding: 4px 7px;
  font-size: 8px; font-family: 'Inter',sans-serif; color: #c8d8e8;
  white-space: nowrap; pointer-events: none;
  box-shadow: 0 3px 10px rgba(0,0,0,0.5); line-height: 1.5;
}
.mk-chip-a { top: 15%; left: 44%; animation: mk-chip-a 3.8s ease-in-out infinite; }
.mk-chip-b { top: 62%; left: 14%; animation: mk-chip-b 4.5s ease-in-out infinite 1.3s; }
.mk-chip-hot  { color: #ff7043; font-weight: 700; }
.mk-chip-cool { color: #81c784; font-weight: 700; }
/* RIGHT SIDEBAR */
.mk-right {
  width: 100px; flex-shrink: 0; background: #f2f4f7;
  border-left: 1px solid rgba(0,0,0,0.07);
  padding: 8px 7px; display: flex; flex-direction: column; gap: 6px;
  overflow: hidden;
}
.mk-r-label  { height: 4px; border-radius: 2px; background: rgba(0,0,0,0.25); width: 65%; margin-bottom: 2px; }
.mk-r-grad   { height: 5px; border-radius: 3px; background: linear-gradient(to right,#FFFFB2,#FECC5C,#FD8D3C,#F03B20,#BD0026); margin-bottom: 3px; }
.mk-r-lo-hi  { display: flex; justify-content: space-between; margin-bottom: 6px; }
.mk-r-tick   { height: 3px; border-radius: 1px; background: rgba(0,0,0,0.12); width: 28%; }
.mk-r-row    { display: flex; align-items: center; gap: 3px; margin-bottom: 2px; }
.mk-r-rank   { width: 7px; height: 3px; border-radius: 1px; background: rgba(0,0,0,0.20); flex-shrink: 0; }
.mk-r-name   { flex: 1; height: 3px; border-radius: 1px; background: rgba(0,0,0,0.12); }
.mk-r-score  { width: 12px; height: 3px; border-radius: 1px; flex-shrink: 0; }
"""

NEW_MOCKUP_HTML = """      <div class="hero-mockup-wrap">
        <div class="hero-mockup-card" id="hero-mockup-card">
          <div class="mockup-titlebar">
            <span class="mockup-dot mockup-dot-r"></span>
            <span class="mockup-dot mockup-dot-y"></span>
            <span class="mockup-dot mockup-dot-g"></span>
            <span class="mockup-titlebar-label">UGPI Barcelona &middot; Interactive Map</span>
          </div>
          <div class="mockup-body">

            <!-- LEFT SIDEBAR -->
            <div class="mk-left">
              <div class="mk-title"></div>
              <div class="mk-sub"></div>
              <div class="mk-search">
                <div class="mk-search-icon"></div>
                <div class="mk-search-bar"></div>
              </div>
              <div class="mk-dot-row"><div class="mk-dot" style="background:rgba(255,112,67,0.7)"></div><div class="mk-dotlabel" style="width:55%"></div></div>
              <div class="mk-dot-row"><div class="mk-dot" style="background:rgba(100,180,100,0.7)"></div><div class="mk-dotlabel" style="width:75%"></div></div>
              <div class="mk-dot-row"><div class="mk-dot" style="background:rgba(126,184,212,0.7)"></div><div class="mk-dotlabel" style="width:65%"></div></div>
              <div class="mk-sep"></div>
              <div class="mk-label"></div>
              <div class="mk-btn-grid">
                <div class="mk-btn on"></div>
                <div class="mk-btn"></div>
                <div class="mk-btn"></div>
                <div class="mk-btn"></div>
              </div>
              <div class="mk-sep"></div>
              <div class="mk-label" style="width:70%"></div>
              <div class="mk-btn-full"></div>
              <div class="mk-btn-full"></div>
              <div class="mk-btn-full"></div>
              <div class="mk-sep"></div>
              <div class="mk-label" style="width:62%"></div>
              <div class="mk-slider-row">
                <div class="mk-slider-dot" style="background:rgba(255,112,67,0.8)"></div>
                <div class="mk-slider-track"><div class="mk-slider-fill" style="background:rgba(255,112,67,0.5)"></div><div class="mk-slider-thumb"></div></div>
              </div>
              <div class="mk-slider-row">
                <div class="mk-slider-dot" style="background:rgba(100,180,90,0.8)"></div>
                <div class="mk-slider-track"><div class="mk-slider-fill" style="background:rgba(100,180,90,0.5)"></div><div class="mk-slider-thumb"></div></div>
              </div>
              <div class="mk-slider-row">
                <div class="mk-slider-dot" style="background:rgba(126,184,212,0.8)"></div>
                <div class="mk-slider-track"><div class="mk-slider-fill" style="background:rgba(126,184,212,0.5)"></div><div class="mk-slider-thumb"></div></div>
              </div>
              <div class="mk-bottom">
                <div class="mk-bottom-btn export"></div>
                <div class="mk-bottom-btn how"></div>
              </div>
            </div>

            <!-- MAP -->
            <div class="mk-map">
              <div class="mk-map-grid" id="mockup-grid"></div>
              <div class="mk-zoom">
                <div class="mk-zoom-btn">+</div>
                <div class="mk-zoom-btn">−</div>
              </div>
              <div class="mk-scan"></div>
              <div class="mk-chip mk-chip-a">Nou Barris &middot; <span class="mk-chip-hot">7.1</span></div>
              <div class="mk-chip mk-chip-b">Sarrià &middot; <span class="mk-chip-cool">5.9</span></div>
            </div>

            <!-- RIGHT SIDEBAR -->
            <div class="mk-right">
              <div class="mk-r-label"></div>
              <div class="mk-r-grad"></div>
              <div class="mk-r-lo-hi"><div class="mk-r-tick"></div><div class="mk-r-tick"></div></div>
              <div class="mk-r-label" style="width:80%; margin-top:4px;"></div>
              <div class="mk-r-row"><div class="mk-r-rank"></div><div class="mk-r-name"></div><div class="mk-r-score" style="background:rgba(255,180,60,0.7)"></div></div>
              <div class="mk-r-row"><div class="mk-r-rank"></div><div class="mk-r-name"></div><div class="mk-r-score" style="background:rgba(255,170,50,0.65)"></div></div>
              <div class="mk-r-row"><div class="mk-r-rank"></div><div class="mk-r-name"></div><div class="mk-r-score" style="background:rgba(255,160,45,0.65)"></div></div>
              <div class="mk-r-row"><div class="mk-r-rank"></div><div class="mk-r-name"></div><div class="mk-r-score" style="background:rgba(255,150,40,0.60)"></div></div>
              <div class="mk-r-row"><div class="mk-r-rank"></div><div class="mk-r-name"></div><div class="mk-r-score" style="background:rgba(254,200,80,0.60)"></div></div>
              <div class="mk-r-row"><div class="mk-r-rank"></div><div class="mk-r-name"></div><div class="mk-r-score" style="background:rgba(254,200,80,0.55)"></div></div>
              <div class="mk-r-row"><div class="mk-r-rank"></div><div class="mk-r-name"></div><div class="mk-r-score" style="background:rgba(254,190,70,0.55)"></div></div>
              <div class="mk-r-row"><div class="mk-r-rank"></div><div class="mk-r-name"></div><div class="mk-r-score" style="background:rgba(254,190,70,0.50)"></div></div>
              <div class="mk-r-row"><div class="mk-r-rank"></div><div class="mk-r-name"></div><div class="mk-r-score" style="background:rgba(254,180,60,0.50)"></div></div>
              <div class="mk-r-row"><div class="mk-r-rank"></div><div class="mk-r-name"></div><div class="mk-r-score" style="background:rgba(100,180,100,0.55)"></div></div>
              <div style="height:1px;background:rgba(0,0,0,0.07);margin:4px 0;"></div>
              <div class="mk-r-label" style="width:70%;"></div>
              <div class="mk-r-row"><div class="mk-r-rank"></div><div class="mk-r-name"></div><div class="mk-r-score" style="background:rgba(240,59,32,0.8)"></div></div>
              <div class="mk-r-row"><div class="mk-r-rank"></div><div class="mk-r-name"></div><div class="mk-r-score" style="background:rgba(240,59,32,0.75)"></div></div>
              <div class="mk-r-row"><div class="mk-r-rank"></div><div class="mk-r-name"></div><div class="mk-r-score" style="background:rgba(240,59,32,0.70)"></div></div>
            </div>
          </div>
        </div>
      </div><!-- /hero-mockup-wrap -->"""

# Map grid JS (replaces old one — uses geographic distribution matching screenshot)
NEW_GRID_JS = """
  // Hero mockup map grid — realistic UGPI distribution
  var grid = document.getElementById('mockup-grid');
  if (grid) {
    var seed = 137;
    function rnd() { seed=(seed*1664525+1013904223)&0xffffffff; return (seed>>>0)/0xffffffff; }
    // Barcelona UGPI: north-east = hot (red), north-west = moderate (orange),
    // south-centre/west = lower (yellow), water/mountain = dark base
    var palette = [
      '#FFFFB2','#FECC5C','#FECC5C','#FD8D3C','#FD8D3C','#FD8D3C',
      '#F03B20','#F03B20','#BD0026','#BD0026','#BD0026','#1a2535'
    ];
    var cols=18, rows=13, html='';
    for(var r=0;r<rows;r++) {
      for(var c=0;c<cols;c++) {
        // NE corner = highest scores, NW = mountain (dark), SE = high, SW = lower
        var ne = (c/cols)*(1-r/rows);          // high in NE
        var nw = (1-c/cols)*(1-r/rows)*0.5;    // mountain NW
        var heat = Math.min(1, ne*1.4 + rnd()*0.3);
        var isMtn = (c<4 && r<6 && rnd()>0.5); // Collserola mountains (NW)
        var isSea = (c>14 && r>9 && rnd()>0.4); // Mediterranean (SE)
        var idx;
        if(isMtn||isSea) { idx=11; }
        else { idx=Math.min(11,Math.floor(heat*11)); }
        var op=(0.5+rnd()*0.5).toFixed(2);
        html+='<div class="mk-cell" style="background:'+palette[idx]+';opacity:'+op+'"></div>';
      }
    }
    grid.innerHTML=html;
  }
  // Mouse-parallax tilt
  var card=document.getElementById('hero-mockup-card');
  if(card){var wrap=card.parentElement;wrap.addEventListener('mousemove',function(e){var r=wrap.getBoundingClientRect(),dx=(e.clientX-r.left-r.width/2)/(r.width/2),dy=(e.clientY-r.top-r.height/2)/(r.height/2);card.style.transform='perspective(1100px) rotateX('+(6-dy*7)+'deg) rotateY('+(-14+dx*9)+'deg) rotateZ(1deg)';});wrap.addEventListener('mouseleave',function(){card.style.transform='perspective(1100px) rotateX(6deg) rotateY(-14deg) rotateZ(1deg)';});}"""

# ─────────────────────────────────────────────────────────────────────
# 2. BIGGER SATELLITE ORBIT (180→300 px)
# ─────────────────────────────────────────────────────────────────────
NEW_SAT_SVG = """      <div class="sat-orbit-deco" aria-hidden="true" style="width:300px;height:300px;top:-60px;right:-80px;">
        <svg viewBox="0 0 180 180" xmlns="http://www.w3.org/2000/svg" fill="none">
          <circle cx="90" cy="90" r="18" fill="#1b3a4b" stroke="rgba(126,184,212,0.5)" stroke-width="1.5"/>
          <circle cx="90" cy="90" r="18" fill="none" stroke="rgba(126,184,212,0.2)" stroke-width="6"/>
          <ellipse cx="90" cy="90" rx="64" ry="26" stroke="rgba(126,184,212,0.18)" stroke-width="1" transform="rotate(-20 90 90)"/>
          <ellipse cx="90" cy="90" rx="50" ry="20" stroke="rgba(126,184,212,0.14)" stroke-width="1" transform="rotate(40 90 90)"/>
          <ellipse cx="90" cy="90" rx="76" ry="30" stroke="rgba(126,184,212,0.12)" stroke-width="1" transform="rotate(10 90 90)"/>
          <g style="transform-origin:90px 90px; animation:sat-orbit-a 7s linear infinite">
            <rect x="87" y="22" width="6" height="4" rx="1" fill="#7eb8d4"/>
            <rect x="82" y="23.5" width="5" height="1" rx="0.5" fill="rgba(126,184,212,0.5)"/>
            <rect x="93" y="23.5" width="5" height="1" rx="0.5" fill="rgba(126,184,212,0.5)"/>
          </g>
          <g style="transform-origin:90px 90px; animation:sat-orbit-b 10s linear infinite">
            <rect x="87" y="36" width="6" height="4" rx="1" fill="#a0d48d"/>
            <rect x="82" y="37.5" width="5" height="1" rx="0.5" fill="rgba(160,212,141,0.5)"/>
            <rect x="93" y="37.5" width="5" height="1" rx="0.5" fill="rgba(160,212,141,0.5)"/>
          </g>
          <g style="transform-origin:90px 90px; animation:sat-orbit-c 13s linear infinite">
            <rect x="87" y="10" width="6" height="4" rx="1" fill="#ff7043"/>
            <rect x="82" y="11.5" width="5" height="1" rx="0.5" fill="rgba(255,112,67,0.5)"/>
            <rect x="93" y="11.5" width="5" height="1" rx="0.5" fill="rgba(255,112,67,0.5)"/>
          </g>
        </svg>
      </div>"""

# ─────────────────────────────────────────────────────────────────────
# 3. METHODOLOGY HERO DECORATION — data-pipeline SVG
# ─────────────────────────────────────────────────────────────────────
METH_DECO_CSS = """
/* ── Methodology hero decoration ────────────────────────── */
@media (min-width: 1040px) {
  #hero .hero-inner { display: flex !important; align-items: center; gap: 80px; max-width:1280px !important; }
  #hero .hero-text  { flex: 0 0 500px; }
  #hero .meth-deco-wrap { flex: 1; display: flex; justify-content: center; align-items: center; }
}
@media (max-width: 1039px) { .meth-deco-wrap { display: none; } }
@keyframes pipe-flow {
  0%   { stroke-dashoffset: 24; }
  100% { stroke-dashoffset: 0; }
}
@keyframes node-glow {
  0%,100% { filter: drop-shadow(0 0 6px currentColor); opacity: 0.85; }
  50%      { filter: drop-shadow(0 0 14px currentColor); opacity: 1; }
}
@keyframes result-pulse {
  0%,100% { r: 28; }
  50%      { r: 31; }
}
"""

METH_DECO_HTML = """
          <div class="meth-deco-wrap" aria-hidden="true">
            <svg viewBox="0 0 320 340" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:320px;height:340px">
              <!-- Source nodes -->
              <!-- Landsat -->
              <rect x="18" y="20" width="80" height="52" rx="8"
                    fill="rgba(255,112,67,0.10)" stroke="rgba(255,112,67,0.55)" stroke-width="1.5"
                    style="animation:node-glow 3s ease-in-out infinite;color:#ff7043"/>
              <text x="58" y="42" text-anchor="middle" font-family="Inter,sans-serif" font-size="9.5" font-weight="700" fill="#ff7043" letter-spacing="0.05em">LANDSAT</text>
              <text x="58" y="57" text-anchor="middle" font-family="Inter,sans-serif" font-size="8.5" fill="rgba(255,255,255,0.45)">30 m LST</text>

              <!-- Sentinel-2 -->
              <rect x="120" y="20" width="80" height="52" rx="8"
                    fill="rgba(100,187,106,0.10)" stroke="rgba(100,187,106,0.55)" stroke-width="1.5"
                    style="animation:node-glow 3.4s ease-in-out infinite 0.6s;color:#64bb6a"/>
              <text x="160" y="42" text-anchor="middle" font-family="Inter,sans-serif" font-size="9.5" font-weight="700" fill="#64bb6a" letter-spacing="0.05em">SENTINEL-2</text>
              <text x="160" y="57" text-anchor="middle" font-family="Inter,sans-serif" font-size="8.5" fill="rgba(255,255,255,0.45)">10 m NDVI</text>

              <!-- Idescat -->
              <rect x="222" y="20" width="80" height="52" rx="8"
                    fill="rgba(126,184,212,0.10)" stroke="rgba(126,184,212,0.55)" stroke-width="1.5"
                    style="animation:node-glow 3.8s ease-in-out infinite 1.2s;color:#7eb8d4"/>
              <text x="262" y="42" text-anchor="middle" font-family="Inter,sans-serif" font-size="9.5" font-weight="700" fill="#7eb8d4" letter-spacing="0.05em">IDESCAT</text>
              <text x="262" y="57" text-anchor="middle" font-family="Inter,sans-serif" font-size="8.5" fill="rgba(255,255,255,0.45)">Census data</text>

              <!-- Down arrows from sources -->
              <line x1="58"  y1="72" x2="58"  y2="108" stroke="rgba(255,112,67,0.50)" stroke-width="1.5" stroke-dasharray="4 3" style="animation:pipe-flow 1.2s linear infinite"/>
              <line x1="160" y1="72" x2="160" y2="108" stroke="rgba(100,187,106,0.50)" stroke-width="1.5" stroke-dasharray="4 3" style="animation:pipe-flow 1.2s linear infinite 0.4s"/>
              <line x1="262" y1="72" x2="262" y2="108" stroke="rgba(126,184,212,0.50)" stroke-width="1.5" stroke-dasharray="4 3" style="animation:pipe-flow 1.2s linear infinite 0.8s"/>

              <!-- Normalize boxes -->
              <rect x="20"  y="108" width="76" height="34" rx="6" fill="rgba(255,112,67,0.07)"  stroke="rgba(255,112,67,0.30)"  stroke-width="1"/>
              <text x="58"  y="129" text-anchor="middle" font-family="Inter,sans-serif" font-size="9" fill="rgba(255,255,255,0.55)">Normalize 1–10</text>
              <rect x="122" y="108" width="76" height="34" rx="6" fill="rgba(100,187,106,0.07)" stroke="rgba(100,187,106,0.30)" stroke-width="1"/>
              <text x="160" y="129" text-anchor="middle" font-family="Inter,sans-serif" font-size="9" fill="rgba(255,255,255,0.55)">Normalize 1–10</text>
              <rect x="224" y="108" width="76" height="34" rx="6" fill="rgba(126,184,212,0.07)" stroke="rgba(126,184,212,0.30)" stroke-width="1"/>
              <text x="262" y="129" text-anchor="middle" font-family="Inter,sans-serif" font-size="9" fill="rgba(255,255,255,0.55)">Normalize 1–10</text>

              <!-- Converging lines to center -->
              <polyline points="58,142 58,195 160,195"  stroke="rgba(180,180,180,0.25)" stroke-width="1.5" stroke-dasharray="4 3" style="animation:pipe-flow 1.4s linear infinite"/>
              <line x1="160" y1="142" x2="160" y2="195" stroke="rgba(180,180,180,0.30)" stroke-width="1.5" stroke-dasharray="4 3" style="animation:pipe-flow 1.4s linear infinite 0.3s"/>
              <polyline points="262,142 262,195 160,195" stroke="rgba(180,180,180,0.25)" stroke-width="1.5" stroke-dasharray="4 3" style="animation:pipe-flow 1.4s linear infinite 0.6s"/>

              <!-- Weighted average box -->
              <rect x="80" y="195" width="160" height="38" rx="8"
                    fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.20)" stroke-width="1.5"/>
              <text x="160" y="210" text-anchor="middle" font-family="Inter,sans-serif" font-size="9.5" font-weight="600" fill="rgba(255,255,255,0.70)" letter-spacing="0.04em">WEIGHTED AVERAGE</text>
              <text x="160" y="224" text-anchor="middle" font-family="Inter,sans-serif" font-size="8.5" fill="rgba(255,255,255,0.35)">33% &nbsp;·&nbsp; 33% &nbsp;·&nbsp; 34%</text>

              <!-- Final arrow -->
              <line x1="160" y1="233" x2="160" y2="267" stroke="rgba(254,204,92,0.60)" stroke-width="2" stroke-dasharray="5 3" style="animation:pipe-flow 1s linear infinite"/>

              <!-- UGPI result node -->
              <circle cx="160" cy="295" r="28" fill="rgba(254,204,92,0.10)" stroke="rgba(254,204,92,0.65)" stroke-width="2" style="animation:result-pulse 2.5s ease-in-out infinite"/>
              <text x="160" y="291" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" font-weight="700" fill="#fecc5c">UGPI</text>
              <text x="160" y="306" text-anchor="middle" font-family="Inter,sans-serif" font-size="8.5" fill="rgba(254,204,92,0.60)">Score 1–10</text>
            </svg>
          </div>"""

# ─────────────────────────────────────────────────────────────────────
# 4. NAV DROPDOWN CSS + HTML
# ─────────────────────────────────────────────────────────────────────
NAV_DD_CSS = """
/* ── Nav dropdown ────────────────────────────────────────── */
.nav-dd-item { position: relative; }
.nav-dd-trigger { display: inline-flex !important; align-items: center; gap: 4px; cursor: pointer; }
.nav-dd-chevron { transition: transform 0.2s; flex-shrink: 0; }
.nav-dd-item:hover .nav-dd-chevron { transform: rotate(180deg); }
.nav-dd {
  position: absolute; top: 100%; left: 50%;
  transform: translateX(-50%) translateY(-4px);
  background: rgba(18,20,20,0.97);
  backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255,255,255,0.10); border-radius: 10px;
  padding: 8px 0; min-width: 215px; list-style: none;
  opacity: 0; visibility: hidden; pointer-events: none;
  transition: opacity 0.18s ease, transform 0.18s ease;
  box-shadow: 0 12px 40px rgba(0,0,0,0.55); z-index: 9999;
}
.nav-dd-item:hover .nav-dd {
  opacity: 1; visibility: visible; pointer-events: auto;
  transform: translateX(-50%) translateY(0);
}
.nav-dd li a {
  display: flex !important; align-items: center; gap: 10px;
  padding: 9px 18px !important;
  font-family: 'Space Grotesk',sans-serif !important;
  font-size: 12px !important; font-weight: 500 !important;
  letter-spacing: 0.05em !important; text-transform: uppercase !important;
  color: var(--on-surface-variant) !important;
  transition: background 0.15s, color 0.15s !important;
  text-decoration: none !important;
}
.nav-dd li a:hover { background: rgba(255,255,255,0.06) !important; color: var(--primary) !important; }
.nav-dd-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
"""

NAV_OLD = '<li><a href="methodology.html">Methodology</a></li>'
NAV_NEW = """<li class="nav-dd-item">
      <a href="methodology.html" class="nav-dd-trigger">Methodology
        <svg class="nav-dd-chevron" width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><polyline points="2,3 5,7 8,3"/></svg>
      </a>
      <ul class="nav-dd">
        <li><a href="heat.html"><span class="nav-dd-dot" style="background:#ff7043"></span>Heat Layer</a></li>
        <li><a href="green.html"><span class="nav-dd-dot" style="background:#a0d48d"></span>Green Space</a></li>
        <li><a href="social.html"><span class="nav-dd-dot" style="background:#7eb8d4"></span>Social Vulnerability</a></li>
      </ul>
    </li>"""

# ─────────────────────────────────────────────────────────────────────
# 5. SCROLL PROGRESS CSS / HTML / JS
# ─────────────────────────────────────────────────────────────────────
PROGRESS_CSS = """
#scroll-progress {
  position: fixed; top: 0; left: 0; height: 3px;
  background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
  z-index: 99999; width: 0%; pointer-events: none; transition: width 0.06s linear;
}
"""
PROGRESS_HTML = '<div id="scroll-progress"></div>\n'
PROGRESS_JS = """<script>
(function(){
  var b=document.getElementById('scroll-progress');
  if(!b) return;
  window.addEventListener('scroll',function(){
    var s=document.documentElement.scrollTop||document.body.scrollTop;
    var t=document.documentElement.scrollHeight-document.documentElement.clientHeight;
    b.style.width=(t>0?s/t*100:0)+'%';
  },{passive:true});
})();
</script>
"""

# ─────────────────────────────────────────────────────────────────────
# APPLY ALL CHANGES
# ─────────────────────────────────────────────────────────────────────

def add_scroll_progress(html):
    """Add progress bar CSS + element + JS if not present."""
    if 'scroll-progress' in html:
        return html
    html = html.replace('</style>\n</head>', PROGRESS_CSS + '</style>\n</head>', 1)
    html = html.replace('<body>\n', '<body>\n' + PROGRESS_HTML, 1)
    html = html.replace('</body>', PROGRESS_JS + '</body>', 1)
    return html

def add_nav_dropdown(html):
    """Replace plain Methodology link with dropdown."""
    if 'nav-dd-item' in html:
        return html
    html = html.replace('</style>\n</head>', NAV_DD_CSS + '</style>\n</head>', 1)
    html = html.replace(NAV_OLD, NAV_NEW, 1)
    return html

# ── INDEX.HTML ─────────────────────────────────────────────────────
with open('outputs/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace old mockup CSS block — find between the CSS comment and next comment
html = re.sub(
    r'/\* ── Hero mockup card ─+\*/.*?/\* ── District map section',
    NEW_MOCKUP_CSS + '\n/* ── District map section',
    html, count=1, flags=re.DOTALL
)

# Replace old mockup HTML block (from <div class="hero-mockup-wrap"> to <!-- /hero-mockup-wrap -->)
html = re.sub(
    r'      <div class="hero-mockup-wrap">.*?</div><!-- /hero-mockup-wrap -->',
    NEW_MOCKUP_HTML,
    html, count=1, flags=re.DOTALL
)

# Replace old grid+parallax JS block
html = re.sub(
    r'  // Hero mockup grid.*?card\.style\.transform=.*?\}\}',
    NEW_GRID_JS,
    html, count=1, flags=re.DOTALL
)

# Enlarge satellite orbit
html = html.replace(
    '<div class="sat-orbit-deco" aria-hidden="true">',
    NEW_SAT_SVG.split('\n')[0]  # just replace the opening div
)
# Replace entire old sat-orbit-deco
html = re.sub(
    r'      <div class="sat-orbit-deco".*?</div>\n',
    NEW_SAT_SVG + '\n',
    html, count=1, flags=re.DOTALL
)

html = add_nav_dropdown(html)

with open('outputs/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html done')

# ── METHODOLOGY.HTML ───────────────────────────────────────────────
with open('outputs/methodology.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = add_scroll_progress(html)
html = add_nav_dropdown(html)

# Add deco CSS
html = html.replace('</style>\n</head>', METH_DECO_CSS + '</style>\n</head>', 1)

# Wrap hero text content + inject deco
HERO_INNER_OLD = '    <div class="hero-inner">\n\n      <div class="hero-label reveal">'
HERO_INNER_NEW = '    <div class="hero-inner">\n      <div class="hero-text">\n\n      <div class="hero-label reveal">'
html = html.replace(HERO_INNER_OLD, HERO_INNER_NEW, 1)

# Find end of hero-inner content (pills-row closing + hero-inner closing)
METH_PILLS_CLOSE = '      </div>\n\n    </div>\n  </section>\n\n  <!-- FORMULA'
METH_PILLS_NEW   = '      </div>\n\n      </div><!-- /hero-text -->\n' + METH_DECO_HTML + '\n\n    </div>\n  </section>\n\n  <!-- FORMULA'
html = html.replace(METH_PILLS_CLOSE, METH_PILLS_NEW, 1)

with open('outputs/methodology.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('methodology.html done')

# ── VALIDATION + ABOUT ─────────────────────────────────────────────
for fname in ['validation.html', 'about.html']:
    with open(f'outputs/{fname}', 'r', encoding='utf-8') as f:
        html = f.read()
    html = add_scroll_progress(html)
    html = add_nav_dropdown(html)
    with open(f'outputs/{fname}', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} done')

# ── LAYER PAGES (nav dropdown only — they already have progress bar) ──
for fname in ['heat.html', 'green.html', 'social.html']:
    with open(f'outputs/{fname}', 'r', encoding='utf-8') as f:
        html = f.read()
    html = add_nav_dropdown(html)
    with open(f'outputs/{fname}', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} nav done')

print('\nAll done.')
