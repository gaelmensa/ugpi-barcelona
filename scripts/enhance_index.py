"""
Visual enhancements for index.html:
  1. Scroll progress bar
  2. Animated stat counters
  3. Hero floating UI mockup (right side)
  4. Barcelona district SVG map (real geometry, 3D tilt)
  5. Satellite orbit animation in data sources section
  6. Staggered card reveals
  7. Parallax on hero glows
"""

with open('outputs/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ─────────────────────────────────────────────────────────────────────
# CSS to inject (before </style> of the main style block)
# ─────────────────────────────────────────────────────────────────────
NEW_CSS = """
/* ── Scroll progress bar ──────────────────────────────────── */
#scroll-progress {
  position: fixed; top: 0; left: 0; height: 3px;
  background: linear-gradient(90deg, var(--primary) 0%, #a8d87a 50%, #fecc5c 100%);
  z-index: 99999; width: 0%; pointer-events: none;
  transition: width 0.06s linear;
}

/* ── Hero flex layout (desktop only) ─────────────────────── */
@media (min-width: 1040px) {
  .hero-inner {
    display: flex !important; align-items: center; gap: 80px;
    max-width: 1300px !important;
  }
  .hero-text { flex: 0 0 510px; }
  .hero-mockup-wrap { flex: 1; display: flex; justify-content: center; align-items: center; }
}
@media (max-width: 1039px) { .hero-mockup-wrap { display: none; } }

/* ── Hero mockup card ─────────────────────────────────────── */
.hero-mockup-card {
  width: 430px; height: 285px;
  background: #081420;
  border-radius: 12px;
  border: 1px solid rgba(126,184,212,0.22);
  box-shadow: 0 0 90px rgba(126,184,212,0.07), 0 28px 70px rgba(0,0,0,0.7);
  transform: perspective(1100px) rotateX(6deg) rotateY(-14deg) rotateZ(1deg);
  transition: transform 0.55s cubic-bezier(.23,1,.32,1), box-shadow 0.55s;
  overflow: hidden; position: relative; will-change: transform;
}
.mockup-titlebar {
  height: 26px; background: rgba(255,255,255,0.03);
  border-bottom: 1px solid rgba(255,255,255,0.06);
  display: flex; align-items: center; padding: 0 10px; gap: 5px; flex-shrink: 0;
}
.mockup-dot { width: 8px; height: 8px; border-radius: 50%; }
.mockup-dot-r { background: #ff5f57; }
.mockup-dot-y { background: #ffbd2e; }
.mockup-dot-g { background: #28ca41; }
.mockup-titlebar-label {
  margin-left: 8px; font-size: 9px; color: rgba(255,255,255,0.20);
  font-family: 'Inter',sans-serif; letter-spacing: 0.06em;
}
.mockup-body { display: flex; height: calc(100% - 26px); }
.mockup-sidebar-strip {
  width: 52px; flex-shrink: 0;
  border-right: 1px solid rgba(255,255,255,0.055);
  padding: 8px 6px; display: flex; flex-direction: column; gap: 5px;
}
.mss-block { height: 6px; border-radius: 2px; background: rgba(255,255,255,0.07); }
.mss-teal  { height: 6px; border-radius: 2px; background: rgba(126,184,212,0.28); }
.mss-spacer { flex: 1; }
.mss-grid  { display: grid; grid-template-columns: 1fr 1fr; gap: 3px; margin-top: 6px; }
.mss-btn   { height: 17px; border-radius: 3px; background: rgba(255,255,255,0.05); }
.mss-btn.on{ background: rgba(255,255,255,0.78); }
.mockup-map-area { flex: 1; position: relative; overflow: hidden; }
.mockup-grid {
  display: grid; grid-template-columns: repeat(20,1fr);
  gap: 0.7px; width: 100%; height: 100%;
}
.mg-cell { transition: opacity 0.4s; }
@keyframes mockup-scan {
  0%   { left: -20%; }
  100% { left: 120%; }
}
.mockup-scan {
  position: absolute; top: 0; bottom: 0; width: 44px;
  background: linear-gradient(90deg,transparent,rgba(126,184,212,0.13),transparent);
  animation: mockup-scan 5.5s ease-in-out infinite 1.5s;
  pointer-events: none; z-index: 2;
}
.mockup-right-panel {
  width: 56px; flex-shrink: 0;
  border-left: 1px solid rgba(255,255,255,0.055);
  padding: 8px 6px; display: flex; flex-direction: column; gap: 7px;
}
.mrp-label {
  font-size: 6px; color: rgba(126,184,212,0.60);
  letter-spacing: 0.12em; text-transform: uppercase; font-family: 'Inter',sans-serif;
}
.mrp-bar-track { height: 3px; border-radius: 2px; background: rgba(255,255,255,0.08); overflow: hidden; margin-top: 2px; }
.mrp-bar-fill  { height: 100%; border-radius: 2px; }
@keyframes chip-bob-a { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-5px)} }
@keyframes chip-bob-b { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-4px)} }
.mockup-chip {
  position: absolute; z-index: 5;
  background: rgba(8,20,32,0.94); border: 1px solid rgba(126,184,212,0.40);
  border-radius: 7px; padding: 5px 9px;
  font-size: 9px; font-family: 'Inter',sans-serif; color: #c8d8e8;
  white-space: nowrap; pointer-events: none;
  box-shadow: 0 4px 14px rgba(0,0,0,0.55); line-height: 1.5;
}
.chip-a { top: 16%; left: 48%; animation: chip-bob-a 3.8s ease-in-out infinite; }
.chip-b { top: 60%; left: 20%; animation: chip-bob-b 4.5s ease-in-out infinite 1.3s; }
.chip-hot  { color: #ff7043; font-weight: 700; }
.chip-cool { color: #81c784; font-weight: 700; }

/* ── District map section ─────────────────────────────────── */
.district-map-section {
  padding: 108px 48px;
  background: var(--background);
  border-top: 1px solid rgba(255,255,255,0.06);
}
.district-map-inner {
  max-width: 1200px; margin: 0 auto;
  display: grid; grid-template-columns: 1fr 320px; gap: 72px; align-items: center;
}
@media (max-width: 900px) { .district-map-inner { grid-template-columns:1fr; gap:40px; } }
.district-tilt-wrap {
  transform: perspective(900px) rotateX(10deg) rotateY(3deg);
  filter: drop-shadow(0 24px 48px rgba(0,0,0,0.55));
  transition: transform 0.7s cubic-bezier(.23,1,.32,1);
}
.district-tilt-wrap:hover { transform: perspective(900px) rotateX(5deg) rotateY(2deg); }
#district-svg { width: 100%; height: auto; display: block; }
.dist-path {
  cursor: pointer; transition: filter 0.2s, opacity 0.5s;
  opacity: 0;
}
.dist-path:hover { filter: brightness(1.3) drop-shadow(0 0 6px rgba(255,255,255,0.3)); }
.dist-label {
  font-family: 'Inter',sans-serif; font-size: 10.5px; font-weight: 700;
  fill: #fff; text-anchor: middle; dominant-baseline: middle;
  pointer-events: none; opacity: 0; transition: opacity 0.5s;
  paint-order: stroke; stroke: rgba(0,0,0,0.65); stroke-width: 3px;
}
.district-tooltip {
  position: absolute; pointer-events: none;
  background: rgba(8,20,32,0.96); border: 1px solid rgba(126,184,212,0.35);
  border-radius: 9px; padding: 10px 15px;
  font-family: 'Inter',sans-serif; color: #e8edf3;
  box-shadow: 0 8px 28px rgba(0,0,0,0.55);
  opacity: 0; transition: opacity 0.15s; z-index: 10; white-space: nowrap;
}
.dt-name  { font-weight: 700; font-size: 13px; margin-bottom: 2px; }
.dt-score { color: #fecc5c; font-size: 18px; font-weight: 800; }
.dt-rank  { font-size: 10px; color: rgba(255,255,255,0.40); margin-top: 2px; }
.dml-title {
  font-family: 'Space Grotesk',sans-serif; font-size: 28px; font-weight: 700;
  letter-spacing: -0.02em; color: var(--on-surface); margin-bottom: 8px; line-height: 1.2;
}
.dml-sub { font-size: 14px; color: var(--on-surface-variant); line-height: 1.65; margin-bottom: 28px; }
.dml-scale-bar {
  height: 9px; border-radius: 5px;
  background: linear-gradient(to right, #54aa50, #c8b840, #e35950);
  margin-bottom: 6px;
}
.dml-scale-labels {
  display: flex; justify-content: space-between;
  font-size: 10px; color: var(--on-surface-variant); margin-bottom: 24px;
}
.dml-list { display: flex; flex-direction: column; gap: 7px; }
.dml-row  { display: flex; align-items: center; gap: 10px; font-size: 13px; color: var(--on-surface-variant); cursor: default; }
.dml-row:hover { color: var(--on-surface); }
.dml-swatch { width: 10px; height: 10px; border-radius: 3px; flex-shrink: 0; }
.dml-dname  { flex: 1; }
.dml-dscore { font-weight: 700; color: var(--on-surface); }
.dml-drank  { font-size: 10px; min-width: 24px; text-align: right; }

/* ── Satellite orbit ──────────────────────────────────────── */
.innovation-header-wrap { position: relative; }
.sat-orbit-deco {
  position: absolute; top: -40px; right: -60px;
  width: 180px; height: 180px; opacity: 0.45; pointer-events: none;
}
@keyframes sat-orbit-a {
  from { transform: rotate(0deg) translateX(64px) rotate(0deg); }
  to   { transform: rotate(360deg) translateX(64px) rotate(-360deg); }
}
@keyframes sat-orbit-b {
  from { transform: rotate(130deg) translateX(50px) rotate(-130deg); }
  to   { transform: rotate(490deg) translateX(50px) rotate(-490deg); }
}
@keyframes sat-orbit-c {
  from { transform: rotate(250deg) translateX(76px) rotate(-250deg); }
  to   { transform: rotate(610deg) translateX(76px) rotate(-610deg); }
}
"""

# Inject CSS before </style> of the main style block
html = html.replace('</style>\n</head>', NEW_CSS + '\n</style>\n</head>', 1)

# ─────────────────────────────────────────────────────────────────────
# Scroll progress bar HTML
# ─────────────────────────────────────────────────────────────────────
html = html.replace('<body>\n', '<body>\n<div id="scroll-progress"></div>\n', 1)

# ─────────────────────────────────────────────────────────────────────
# Hero: wrap text, add mockup on right
# ─────────────────────────────────────────────────────────────────────
HERO_TEXT_OPEN = '    <div class="hero-inner">\n'
HERO_TEXT_WRAP_OPEN = '    <div class="hero-inner">\n      <div class="hero-text">\n'
html = html.replace(HERO_TEXT_OPEN, HERO_TEXT_WRAP_OPEN, 1)

MOCKUP_HTML = """
      </div><!-- /hero-text -->

      <div class="hero-mockup-wrap">
        <div class="hero-mockup-card" id="hero-mockup-card">
          <div class="mockup-titlebar">
            <span class="mockup-dot mockup-dot-r"></span>
            <span class="mockup-dot mockup-dot-y"></span>
            <span class="mockup-dot mockup-dot-g"></span>
            <span class="mockup-titlebar-label">UGPI Barcelona &middot; Interactive Map</span>
          </div>
          <div class="mockup-body">
            <div class="mockup-sidebar-strip">
              <div class="mss-teal"></div>
              <div class="mss-block" style="width:70%"></div>
              <div class="mss-block" style="width:50%"></div>
              <div class="mss-spacer"></div>
              <div class="mss-grid">
                <div class="mss-btn on"></div>
                <div class="mss-btn"></div>
                <div class="mss-btn"></div>
                <div class="mss-btn"></div>
              </div>
              <div class="mss-block" style="margin-top:8px;width:80%"></div>
              <div class="mss-block" style="width:60%"></div>
              <div class="mss-block" style="width:70%"></div>
            </div>
            <div class="mockup-map-area">
              <div class="mockup-grid" id="mockup-grid"></div>
              <div class="mockup-scan"></div>
              <div class="mockup-chip chip-a">
                Nou Barris &middot; UGPI <span class="chip-hot">7.1</span>
              </div>
              <div class="mockup-chip chip-b">
                Sarrià &middot; UGPI <span class="chip-cool">5.9</span>
              </div>
            </div>
            <div class="mockup-right-panel">
              <div>
                <div class="mrp-label">UGPI</div>
                <div class="mrp-bar-track"><div class="mrp-bar-fill" style="width:68%;background:linear-gradient(90deg,#FECC5C,#F03B20)"></div></div>
              </div>
              <div>
                <div class="mrp-label">Heat</div>
                <div class="mrp-bar-track"><div class="mrp-bar-fill" style="width:72%;background:#ff7043"></div></div>
              </div>
              <div>
                <div class="mrp-label">Green</div>
                <div class="mrp-bar-track"><div class="mrp-bar-fill" style="width:55%;background:#66bb6a"></div></div>
              </div>
              <div>
                <div class="mrp-label">Social</div>
                <div class="mrp-bar-track"><div class="mrp-bar-fill" style="width:61%;background:#7eb8d4"></div></div>
              </div>
            </div>
          </div>
        </div>
      </div><!-- /hero-mockup-wrap -->
"""

# Find end of hero-stats-row and hero-inner close
HERO_STATS_CLOSE = '        <span class="stat-item">No login required</span>\n      </div>\n\n    </div>\n  </section>'
HERO_STATS_NEW   = '        <span class="stat-item">No login required</span>\n      </div>\n' + MOCKUP_HTML + '\n    </div>\n  </section>'
html = html.replace(HERO_STATS_CLOSE, HERO_STATS_NEW, 1)

# ─────────────────────────────────────────────────────────────────────
# District SVG map section (inserted after </div> closing stats-bar)
# ─────────────────────────────────────────────────────────────────────
DISTRICT_DATA = [
    ('Nou Barris',         7.01, '#e35950', 418, 54,
     'M451.2,101.5 L379.6,100.9 L388.1,97.0 L377.8,90.6 L376.5,67.8 L352.3,56.6 L364.0,44.4 L386.0,42.0 L381.3,31.2 L392.0,18.9 L437.6,8.2 L430.8,0.0 L459.3,1.2 L465.6,41.8 L444.2,92.2 L451.2,101.5 Z'),
    ('Sants-Montjuïc',    6.89, '#d46150', 290, 300,
     'M277.0,288.7 L283.5,266.8 L236.9,232.5 L307.8,208.0 L306.8,219.6 L330.0,234.2 L419.2,235.3 L423.4,254.1 L437.8,257.3 L413.0,266.9 L424.1,270.6 L419.7,275.4 L404.3,271.4 L411.5,280.8 L390.6,304.3 L378.5,300.6 L344.2,315.5 L336.1,306.0 L331.4,330.7 L313.4,335.5 L327.6,347.2 L354.4,317.7 L388.3,319.2 L364.3,354.4 L346.5,353.2 L332.5,370.8 L226.9,365.7 L164.3,332.2 L288.3,301.0 L277.0,288.7 Z'),
    ('Sant Andreu',        6.88, '#d36250', 485, 83,
     'M477.4,134.8 L436.7,131.6 L437.8,120.2 L422.1,107.5 L426.1,100.6 L451.2,101.5 L444.2,92.2 L465.4,43.9 L460.2,15.2 L524.9,61.3 L540.1,87.4 L524.3,89.6 L528.2,101.8 L503.5,95.1 L490.8,100.0 L477.4,134.8 Z'),
    ('Horta-Guinardó',    6.73, '#c06d50', 334, 99,
     'M333.3,120.4 L292.3,119.2 L282.3,109.0 L281.2,115.8 L264.6,114.7 L272.3,121.2 L256.5,122.4 L261.0,127.6 L234.6,119.4 L232.2,111.4 L280.9,51.9 L339.7,53.2 L364.0,44.4 L352.3,56.7 L376.5,67.8 L377.8,90.6 L388.1,97.0 L379.4,100.7 L422.1,107.5 L437.8,120.2 L436.7,131.6 L396.5,153.9 L333.3,120.4 Z'),
    ('Gràcia',             6.52, '#a67c50', 340, 148,
     'M352.2,182.5 L317.8,144.1 L266.5,125.4 L264.6,114.7 L281.2,115.8 L282.3,109.0 L298.9,120.5 L330.9,117.1 L339.5,128.9 L358.8,130.0 L408.1,160.5 L352.2,182.5 Z'),
    ('Ciutat Vella',       6.50, '#a37d50', 440, 222,
     'M442.2,245.9 L377.6,224.9 L380.8,208.1 L401.3,208.0 L439.8,191.0 L502.8,209.0 L478.8,224.3 L467.5,243.8 L475.6,247.2 L453.5,277.7 L466.7,255.5 L457.7,261.9 L452.0,258.8 L457.2,222.6 L447.7,220.5 L445.6,236.0 L443.1,222.8 L428.3,236.4 L442.2,245.9 Z'),
    ('Les Corts',          6.38, '#948550', 224, 204,
     'M236.1,231.9 L235.6,226.8 L195.2,231.8 L169.4,218.6 L174.1,210.3 L155.0,186.6 L172.5,168.7 L196.3,183.6 L207.3,178.3 L223.5,183.9 L233.8,196.4 L313.8,190.6 L307.8,208.0 L236.1,231.9 Z'),
    ('Eixample',           6.33, '#8e8950', 383, 192,
     'M326.9,231.2 L306.8,219.6 L315.7,189.3 L392.5,169.1 L408.1,160.5 L396.5,153.9 L419.6,141.2 L455.5,161.2 L458.1,185.0 L401.3,208.0 L380.8,208.1 L377.6,224.9 L393.8,234.4 L326.9,231.2 Z'),
    ('Sant Martí',         6.15, '#779650', 508, 155,
     'M458.1,185.0 L455.5,161.2 L419.6,141.2 L446.6,126.3 L465.8,137.1 L477.4,134.8 L498.8,95.6 L528.2,101.8 L596.4,145.0 L544.0,183.8 L510.1,196.7 L502.8,209.0 L443.4,193.0 L458.1,185.0 Z'),
    ('Sarrià-Sant Gervasi',5.87, '#54aa50', 185, 148,
     'M293.1,193.4 L233.8,196.4 L221.4,183.0 L196.3,183.6 L156.2,148.6 L112.9,147.0 L89.5,163.6 L67.7,162.7 L60.2,153.8 L67.5,143.9 L93.4,132.1 L78.4,116.2 L97.6,111.1 L69.4,108.2 L82.8,99.2 L65.9,80.5 L113.9,98.5 L129.9,99.4 L149.1,87.8 L173.5,100.8 L234.7,106.3 L234.6,119.4 L261.0,127.6 L256.1,122.7 L265.1,122.0 L317.2,143.6 L352.2,182.5 L293.1,193.4 Z'),
]

svg_paths = ''
for name, score, color, cx, cy, path in DISTRICT_DATA:
    svg_paths += f'  <path class="dist-path" data-name="{name}" data-score="{score}" d="{path}" fill="{color}" stroke="#0c1a26" stroke-width="1.2" opacity="0"><title>{name}: {score}</title></path>\n'
    svg_paths += f'  <text class="dist-label" x="{cx}" y="{cy}" opacity="0">{score}</text>\n'

dml_rows = ''
for i, (name, score, color, _, _, _) in enumerate(DISTRICT_DATA):
    rank_txt = f'#{i+1}'
    dml_rows += f'<div class="dml-row"><span class="dml-swatch" style="background:{color}"></span><span class="dml-dname">{name}</span><span class="dml-dscore">{score}</span><span class="dml-drank" style="color:rgba(255,255,255,0.35)">{rank_txt}</span></div>\n'

DISTRICT_SECTION = f"""
  <!-- DISTRICT MAP ════════════════════════════ -->
  <section class="district-map-section">
    <div class="district-map-inner">

      <div style="position:relative;">
        <div class="district-tilt-wrap" id="district-tilt-wrap">
          <svg id="district-svg" viewBox="0 0 600 380" xmlns="http://www.w3.org/2000/svg">
            <rect width="600" height="380" fill="#0c1a26" rx="8"/>
{svg_paths}          </svg>
        </div>
        <div class="district-tooltip" id="district-tooltip">
          <div class="dt-name" id="dt-name">District</div>
          <div class="dt-score" id="dt-score">0.00</div>
          <div class="dt-rank"  id="dt-rank">Rank #0 of 10</div>
        </div>
      </div>

      <div>
        <div class="dml-title reveal">Priority<br>by District</div>
        <p class="dml-sub reveal">Barcelona's 10 districts ranked by composite UGPI score. Higher scores indicate greater urgency for green infrastructure investment.</p>
        <div class="dml-scale-bar reveal"></div>
        <div class="dml-scale-labels reveal"><span>5.87 &mdash; Lower priority</span><span>7.01 &mdash; Critical</span></div>
        <div class="dml-list reveal">
{dml_rows}        </div>
      </div>

    </div>
  </section>
"""

# Insert after the stats-bar closing div
STATS_BAR_CLOSE = '  </div>\n\n  <!-- THE CHALLENGE'
html = html.replace(STATS_BAR_CLOSE, '  </div>\n' + DISTRICT_SECTION + '\n  <!-- THE CHALLENGE', 1)

# ─────────────────────────────────────────────────────────────────────
# Satellite orbit — add to "What Makes It New" section header
# ─────────────────────────────────────────────────────────────────────
SAT_SVG = """
      <div class="sat-orbit-deco" aria-hidden="true">
        <svg viewBox="0 0 180 180" xmlns="http://www.w3.org/2000/svg" fill="none">
          <!-- Earth -->
          <circle cx="90" cy="90" r="18" fill="#1b3a4b" stroke="rgba(126,184,212,0.5)" stroke-width="1.5"/>
          <circle cx="90" cy="90" r="18" fill="none" stroke="rgba(126,184,212,0.2)" stroke-width="6"/>
          <!-- Orbit ellipses -->
          <ellipse cx="90" cy="90" rx="64" ry="26" stroke="rgba(126,184,212,0.18)" stroke-width="1" transform="rotate(-20 90 90)"/>
          <ellipse cx="90" cy="90" rx="50" ry="20" stroke="rgba(126,184,212,0.14)" stroke-width="1" transform="rotate(40 90 90)"/>
          <ellipse cx="90" cy="90" rx="76" ry="30" stroke="rgba(126,184,212,0.12)" stroke-width="1" transform="rotate(10 90 90)"/>
          <!-- Satellites -->
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
      </div>
"""

INNO_OLD = '      <div class="section-header reveal">\n        <span class="label-mono">What Makes It New</span>'
INNO_NEW = '      <div class="section-header reveal" style="position:relative;">\n' + SAT_SVG + '        <span class="label-mono">What Makes It New</span>'
html = html.replace(INNO_OLD, INNO_NEW, 1)

# ─────────────────────────────────────────────────────────────────────
# Staggered reveals on challenge cards (already have them, add more granular)
# Add to the validation stats section
# ─────────────────────────────────────────────────────────────────────
# (they already have reveal-delay-1/2/3 on challenge cards — just verify)

# ─────────────────────────────────────────────────────────────────────
# JavaScript to inject before </body>
# ─────────────────────────────────────────────────────────────────────
NEW_JS = """
<script>
(function() {
  // ── Scroll progress bar ────────────────────────────────
  var bar = document.getElementById('scroll-progress');
  if (bar) {
    window.addEventListener('scroll', function() {
      var scrolled = document.documentElement.scrollTop || document.body.scrollTop;
      var total = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      bar.style.width = (total > 0 ? scrolled / total * 100 : 0) + '%';
    }, { passive: true });
  }

  // ── Stat counters ──────────────────────────────────────
  var _counted = {};
  function countUp(el) {
    var target = parseInt(el.getAttribute('data-target') || '0', 10);
    var duration = target > 500 ? 1600 : 1200;
    var start = performance.now();
    function frame(now) {
      var p = Math.min((now - start) / duration, 1);
      var e = 1 - Math.pow(1 - p, 3);
      var v = Math.round(target * e);
      el.textContent = v.toLocaleString();
      if (p < 1) requestAnimationFrame(frame);
      else el.textContent = target.toLocaleString();
    }
    requestAnimationFrame(frame);
  }
  var cntObs = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      var id = e.target.dataset.target;
      if (e.isIntersecting && !_counted[id]) {
        _counted[id] = true;
        countUp(e.target);
      }
    });
  }, { threshold: 0.6 });
  document.querySelectorAll('.stat-number[data-target]').forEach(function(el) {
    cntObs.observe(el);
  });

  // ── Hero parallax glows ────────────────────────────────
  var glowA = document.querySelector('.hero-glow-a');
  var glowB = document.querySelector('.hero-glow-b');
  if (glowA || glowB) {
    window.addEventListener('scroll', function() {
      var y = window.pageYOffset;
      if (glowA) glowA.style.transform = 'translateY(' + (y * 0.28) + 'px)';
      if (glowB) glowB.style.transform = 'translateY(' + (y * 0.16) + 'px)';
    }, { passive: true });
  }

  // ── Hero mockup grid ───────────────────────────────────
  var grid = document.getElementById('mockup-grid');
  if (grid) {
    // Seeded pseudo-random so it's consistent on reload
    var seed = 42;
    function rand() { seed = (seed * 1664525 + 1013904223) & 0xffffffff; return (seed >>> 0) / 0xffffffff; }
    // UGPI color distribution approximating real data (most tracts 5-8)
    var palette = [
      '#FFFFB2','#FFFFB2','#FECC5C','#FECC5C','#FECC5C','#FECC5C',
      '#FD8D3C','#FD8D3C','#FD8D3C','#F03B20','#F03B20','#BD0026'
    ];
    var html = '';
    for (var i = 0; i < 300; i++) {
      var c = palette[Math.floor(rand() * palette.length)];
      var op = (0.45 + rand() * 0.55).toFixed(2);
      html += '<div class="mg-cell" style="background:' + c + ';opacity:' + op + '"></div>';
    }
    grid.innerHTML = html;
  }

  // ── Hero mockup mouse-parallax tilt ───────────────────
  var card = document.getElementById('hero-mockup-card');
  if (card) {
    var wrap = card.parentElement;
    wrap.addEventListener('mousemove', function(e) {
      var r  = wrap.getBoundingClientRect();
      var dx = (e.clientX - r.left - r.width  / 2) / (r.width  / 2);
      var dy = (e.clientY - r.top  - r.height / 2) / (r.height / 2);
      card.style.transform = 'perspective(1100px) rotateX(' + (6 - dy * 7) + 'deg) rotateY(' + (-14 + dx * 9) + 'deg) rotateZ(1deg)';
    });
    wrap.addEventListener('mouseleave', function() {
      card.style.transform = 'perspective(1100px) rotateX(6deg) rotateY(-14deg) rotateZ(1deg)';
    });
  }

  // ── District SVG map ───────────────────────────────────
  var districtRanks = {
    'Nou Barris':1,'Sants-Montjuïc':2,'Sant Andreu':3,'Horta-Guinardó':4,
    'Gràcia':5,'Ciutat Vella':6,'Les Corts':7,'Eixample':8,'Sant Martí':9,'Sarrià-Sant Gervasi':10
  };
  var svgEl    = document.getElementById('district-svg');
  var tooltip  = document.getElementById('district-tooltip');
  var tiltWrap = document.getElementById('district-tilt-wrap');

  if (svgEl && tooltip) {
    // Animate districts in when section enters viewport
    var distObs = new IntersectionObserver(function(entries) {
      if (!entries[0].isIntersecting) return;
      distObs.disconnect();
      var paths  = svgEl.querySelectorAll('.dist-path');
      var labels = svgEl.querySelectorAll('.dist-label');
      paths.forEach(function(p, i) {
        setTimeout(function() {
          p.style.transition = 'opacity 0.5s ease';
          p.style.opacity    = '1';
        }, i * 80);
      });
      labels.forEach(function(l, i) {
        setTimeout(function() {
          l.style.transition = 'opacity 0.5s ease';
          l.style.opacity    = '1';
        }, i * 80 + 400);
      });
    }, { threshold: 0.2 });
    distObs.observe(svgEl);

    // Tooltip on hover
    svgEl.querySelectorAll('.dist-path').forEach(function(path) {
      path.addEventListener('mouseenter', function(e) {
        var name  = path.dataset.name;
        var score = path.dataset.score;
        var rank  = districtRanks[name] || '?';
        document.getElementById('dt-name').textContent  = name;
        document.getElementById('dt-score').textContent = score;
        document.getElementById('dt-rank').textContent  = 'Rank #' + rank + ' of 10';
        tooltip.style.opacity = '1';
      });
      path.addEventListener('mousemove', function(e) {
        var svgRect = svgEl.getBoundingClientRect();
        var x = e.clientX - svgRect.left + 12;
        var y = e.clientY - svgRect.top  - 20;
        tooltip.style.left = x + 'px';
        tooltip.style.top  = y + 'px';
      });
      path.addEventListener('mouseleave', function() {
        tooltip.style.opacity = '0';
      });
    });

    // Mouse tilt on SVG container
    if (tiltWrap) {
      tiltWrap.addEventListener('mousemove', function(e) {
        var r  = tiltWrap.getBoundingClientRect();
        var dx = (e.clientX - r.left - r.width  / 2) / (r.width  / 2);
        var dy = (e.clientY - r.top  - r.height / 2) / (r.height / 2);
        tiltWrap.style.transform = 'perspective(900px) rotateX(' + (10 - dy * 6) + 'deg) rotateY(' + (3 + dx * 5) + 'deg)';
      });
      tiltWrap.addEventListener('mouseleave', function() {
        tiltWrap.style.transform = 'perspective(900px) rotateX(10deg) rotateY(3deg)';
      });
    }
  }
})();
</script>
"""

html = html.replace('</body>', NEW_JS + '\n</body>', 1)

with open('outputs/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html enhanced.")
