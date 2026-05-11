"""
Visual enhancements for heat.html, green.html, social.html:
  1. Replace horizontal bar charts with animated vertical area charts
  2. Unique hero decorative illustrations per page
  3. Staggered reveals on findings cards
"""

import re

# ─────────────────────────────────────────────────────────────────────
# Shared: animated vertical bar/area chart builder
# ─────────────────────────────────────────────────────────────────────
def make_area_chart(counts, colors, label_lo, label_hi, accent):
    """
    counts: list of 9 integers (score bins 1-2 .. 9-10)
    colors: list of 9 hex colours
    Returns HTML string for an SVG animated bar chart.
    """
    W, H, PAD_L, PAD_B, PAD_T, PAD_R = 560, 220, 44, 32, 12, 12
    inner_w = W - PAD_L - PAD_R
    inner_h = H - PAD_T - PAD_B
    n = len(counts)
    bar_w = inner_w / n
    max_c = max(counts)

    rects = ''
    labels = ''
    for i, (c, col) in enumerate(zip(counts, colors)):
        bh = (c / max_c) * inner_h
        x  = PAD_L + i * bar_w + bar_w * 0.12
        bw = bar_w * 0.76
        y  = PAD_T + inner_h - bh
        rects += (
            f'<rect class="ac-bar" x="{x:.1f}" y="{PAD_T + inner_h:.1f}" width="{bw:.1f}" height="0" '
            f'rx="3" fill="{col}" data-y="{y:.1f}" data-h="{bh:.1f}" '
            f'style="transition:y 0.7s cubic-bezier(.23,1,.32,1) {i*60}ms, height 0.7s cubic-bezier(.23,1,.32,1) {i*60}ms;">'
            f'<title>{i+1}&ndash;{i+2}: {c} tracts</title>'
            f'</rect>\n'
        )
        score_mid = i + 1.5
        lx = PAD_L + (i + 0.5) * bar_w
        labels += f'<text class="ac-axis-label" x="{lx:.1f}" y="{PAD_T + inner_h + 18}" text-anchor="middle">{int(score_mid - 0.5)}</text>\n'

    # y-axis grid lines + labels
    grid = ''
    for step in [0.25, 0.5, 0.75, 1.0]:
        gy = PAD_T + inner_h * (1 - step)
        gv = int(max_c * step)
        grid += f'<line class="ac-grid-line" x1="{PAD_L}" y1="{gy:.1f}" x2="{W - PAD_R}" y2="{gy:.1f}"/>\n'
        grid += f'<text class="ac-axis-label" x="{PAD_L - 6}" y="{gy + 4:.1f}" text-anchor="end">{gv}</text>\n'

    # x-axis line
    grid += f'<line stroke="rgba(255,255,255,0.15)" stroke-width="1" x1="{PAD_L}" y1="{PAD_T+inner_h}" x2="{W-PAD_R}" y2="{PAD_T+inner_h}"/>\n'
    # y-axis line
    grid += f'<line stroke="rgba(255,255,255,0.15)" stroke-width="1" x1="{PAD_L}" y1="{PAD_T}" x2="{PAD_L}" y2="{PAD_T+inner_h}"/>\n'
    # x-axis caption
    grid += f'<text class="ac-axis-label" x="{PAD_L + inner_w/2:.0f}" y="{H}" text-anchor="middle" style="font-size:10px">Score (1 = {label_lo} &nbsp;&nbsp; 10 = {label_hi})</text>\n'

    svg = f'''<svg class="area-chart-svg" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" id="area-chart-svg">
{grid}{rects}{labels}</svg>'''

    return f'<div class="area-chart-wrap" id="bar-chart">\n{svg}\n</div>'


# ─────────────────────────────────────────────────────────────────────
# Data
# ─────────────────────────────────────────────────────────────────────
HEAT_COUNTS  = [1,  4,  13,  94, 440, 435,  64,  13,  3]
HEAT_COLORS  = ['#ffe4cc','#ffd0aa','#ffb880','#ff9a5c','#ff7d42','#ff5722','#e64a19','#d84315','#bf360c']

GREEN_COUNTS = [4,  6,   6,  19,  60, 128, 303, 396, 145]
GREEN_COLORS = ['#dcedc8','#c5e1a5','#aed581','#9ccc65','#8bc34a','#7cb342','#558b2f','#33691e','#1b5e20']

SOCIAL_COUNTS = [0,  3,  45, 127, 400, 414,  75,   4,   0]
SOCIAL_COLORS = ['#e3f2fd','#bbdefb','#90caf9','#64b5f6','#42a5f5','#2196f3','#1e88e5','#1565c0','#0d47a1']

# CSS shared for charts
CHART_CSS = """
/* ── Area chart ─────────────────────────────────────────── */
.area-chart-wrap { position: relative; overflow: visible; }
.area-chart-svg  { width: 100%; height: auto; display: block; overflow: visible; }
.ac-grid-line    { stroke: rgba(255,255,255,0.07); stroke-width: 1; }
.ac-axis-label   { font-family: 'Inter',sans-serif; font-size: 11px; fill: rgba(255,255,255,0.35); }
.ac-bar          { cursor: default; }
.ac-bar:hover    { filter: brightness(1.2); }
"""

# ─────────────────────────────────────────────────────────────────────
# Chart animation JS (shared, injected into each page)
# ─────────────────────────────────────────────────────────────────────
CHART_JS = """
<script>
(function() {
  // Scroll progress bar
  var bar = document.getElementById('scroll-progress');
  if (bar) {
    window.addEventListener('scroll', function() {
      var s = document.documentElement.scrollTop || document.body.scrollTop;
      var t = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      bar.style.width = (t > 0 ? s / t * 100 : 0) + '%';
    }, { passive: true });
  }

  // Area chart bar animation
  var chartEl = document.getElementById('area-chart-svg');
  if (!chartEl) return;
  var obs = new IntersectionObserver(function(entries) {
    if (!entries[0].isIntersecting) return;
    obs.disconnect();
    chartEl.querySelectorAll('.ac-bar').forEach(function(rect) {
      var targetY = parseFloat(rect.dataset.y);
      var targetH = parseFloat(rect.dataset.h);
      rect.setAttribute('y', targetY);
      rect.setAttribute('height', targetH);
    });
  }, { threshold: 0.3 });
  obs.observe(chartEl);
})();
</script>
"""

# ─────────────────────────────────────────────────────────────────────
# Decorative hero illustrations
# ─────────────────────────────────────────────────────────────────────

# Heat: animated sun with radiating rings + city silhouette
HEAT_DECO_CSS = """
/* ── Heat hero decoration ───────────────────────────────── */
.heat-deco-wrap {
  position: absolute; right: 0; top: 50%; transform: translateY(-50%);
  width: 340px; height: 340px; pointer-events: none; opacity: 0.55;
  overflow: visible;
}
@keyframes ring-expand {
  0%   { r: 60; opacity: 0.5; }
  80%  { r: 130; opacity: 0; }
  100% { r: 130; opacity: 0; }
}
@keyframes sun-glow {
  0%, 100% { filter: drop-shadow(0 0 12px rgba(255,112,67,0.6)); }
  50%       { filter: drop-shadow(0 0 24px rgba(255,112,67,0.9)); }
}
@keyframes ray-pulse {
  0%, 100% { opacity: 0.5; }
  50%       { opacity: 1; }
}
@keyframes city-heat {
  0%, 100% { opacity: 0.4; }
  50%       { opacity: 0.6; }
}
"""

HEAT_DECO_HTML = """
        <div class="heat-deco-wrap" aria-hidden="true">
          <svg viewBox="0 0 340 340" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;overflow:visible">
            <!-- Pulsing rings -->
            <circle cx="170" cy="155" r="60" fill="none" stroke="rgba(255,112,67,0.3)" stroke-width="1.5" style="animation:ring-expand 3s ease-out infinite"/>
            <circle cx="170" cy="155" r="60" fill="none" stroke="rgba(255,112,67,0.25)" stroke-width="1" style="animation:ring-expand 3s ease-out infinite 1s"/>
            <circle cx="170" cy="155" r="60" fill="none" stroke="rgba(255,112,67,0.2)" stroke-width="1" style="animation:ring-expand 3s ease-out infinite 2s"/>
            <!-- Sun rays -->
            <g style="transform-origin:170px 155px; animation:ray-pulse 2.5s ease-in-out infinite">
              <line x1="170" y1="88"  x2="170" y2="72"  stroke="rgba(255,200,100,0.7)" stroke-width="2" stroke-linecap="round"/>
              <line x1="170" y1="222" x2="170" y2="238" stroke="rgba(255,200,100,0.7)" stroke-width="2" stroke-linecap="round"/>
              <line x1="103" y1="155" x2="87"  y2="155" stroke="rgba(255,200,100,0.7)" stroke-width="2" stroke-linecap="round"/>
              <line x1="237" y1="155" x2="253" y2="155" stroke="rgba(255,200,100,0.7)" stroke-width="2" stroke-linecap="round"/>
              <line x1="122" y1="108" x2="110" y2="96"  stroke="rgba(255,200,100,0.5)" stroke-width="1.5" stroke-linecap="round"/>
              <line x1="218" y1="108" x2="230" y2="96"  stroke="rgba(255,200,100,0.5)" stroke-width="1.5" stroke-linecap="round"/>
              <line x1="122" y1="202" x2="110" y2="214" stroke="rgba(255,200,100,0.5)" stroke-width="1.5" stroke-linecap="round"/>
              <line x1="218" y1="202" x2="230" y2="214" stroke="rgba(255,200,100,0.5)" stroke-width="1.5" stroke-linecap="round"/>
            </g>
            <!-- Sun body -->
            <circle cx="170" cy="155" r="44" fill="rgba(255,112,67,0.15)" style="animation:sun-glow 3s ease-in-out infinite"/>
            <circle cx="170" cy="155" r="32" fill="rgba(255,140,67,0.25)"/>
            <circle cx="170" cy="155" r="22" fill="rgba(255,160,60,0.6)"/>
            <!-- City silhouette -->
            <g style="animation:city-heat 4s ease-in-out infinite">
              <rect x="30"  y="270" width="18" height="55" fill="rgba(255,112,67,0.25)" rx="1"/>
              <rect x="52"  y="255" width="14" height="70" fill="rgba(255,112,67,0.20)" rx="1"/>
              <rect x="70"  y="268" width="20" height="57" fill="rgba(255,112,67,0.28)" rx="1"/>
              <rect x="94"  y="250" width="16" height="75" fill="rgba(255,112,67,0.22)" rx="1"/>
              <rect x="114" y="262" width="12" height="63" fill="rgba(255,112,67,0.18)" rx="1"/>
              <rect x="230" y="260" width="18" height="65" fill="rgba(255,112,67,0.20)" rx="1"/>
              <rect x="252" y="248" width="14" height="77" fill="rgba(255,112,67,0.25)" rx="1"/>
              <rect x="270" y="263" width="20" height="62" fill="rgba(255,112,67,0.22)" rx="1"/>
              <rect x="294" y="255" width="16" height="70" fill="rgba(255,112,67,0.18)" rx="1"/>
            </g>
          </svg>
        </div>
"""

# Green: animated growing stems with leaves
GREEN_DECO_CSS = """
/* ── Green hero decoration ──────────────────────────────── */
.green-deco-wrap {
  position: absolute; right: 0; top: 0; bottom: 0;
  width: 320px; pointer-events: none; opacity: 0.60; overflow: hidden;
}
@keyframes stem-grow {
  from { stroke-dashoffset: 300; }
  to   { stroke-dashoffset: 0; }
}
@keyframes leaf-unfurl {
  from { transform: scale(0) rotate(-30deg); opacity: 0; }
  to   { transform: scale(1) rotate(0deg);  opacity: 1; }
}
@keyframes leaf-sway {
  0%,100% { transform: rotate(-4deg); }
  50%      { transform: rotate(4deg); }
}
@keyframes ndvi-pulse {
  0%,100% { opacity: 0.6; }
  50%      { opacity: 1; }
}
"""

GREEN_DECO_HTML = """
        <div class="green-deco-wrap" aria-hidden="true">
          <svg viewBox="0 0 320 380" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
            <!-- Main stems -->
            <path d="M160,380 Q155,300 150,240 Q145,180 160,120" stroke="rgba(129,199,132,0.6)" stroke-width="3" stroke-linecap="round" stroke-dasharray="300" style="animation:stem-grow 2s ease-out forwards 0.2s; stroke-dashoffset:300"/>
            <path d="M200,380 Q205,310 210,250 Q215,190 200,130" stroke="rgba(129,199,132,0.5)" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="300" style="animation:stem-grow 2s ease-out forwards 0.5s; stroke-dashoffset:300"/>
            <path d="M120,380 Q115,300 118,240 Q122,175 115,115" stroke="rgba(129,199,132,0.45)" stroke-width="2" stroke-linecap="round" stroke-dasharray="300" style="animation:stem-grow 2s ease-out forwards 0.8s; stroke-dashoffset:300"/>
            <!-- Leaves -->
            <g style="transform-origin:150px 240px; animation:leaf-unfurl 0.8s ease-out forwards 1.8s; opacity:0; transform:scale(0)">
              <ellipse cx="150" cy="240" rx="28" ry="14" fill="rgba(100,180,90,0.55)" transform="rotate(-35 150 240)"/>
            </g>
            <g style="transform-origin:152px 200px; animation:leaf-unfurl 0.8s ease-out forwards 2s; opacity:0; transform:scale(0)">
              <ellipse cx="178" cy="200" rx="26" ry="12" fill="rgba(120,190,80,0.50)" transform="rotate(20 178 200)"/>
            </g>
            <g style="transform-origin:210px 250px; animation:leaf-unfurl 0.8s ease-out forwards 2.2s; opacity:0; transform:scale(0)">
              <ellipse cx="210" cy="250" rx="22" ry="11" fill="rgba(90,170,80,0.48)" transform="rotate(-15 210 250)"/>
            </g>
            <g style="transform-origin:160px 155px; animation:leaf-unfurl 0.8s ease-out forwards 2.4s; opacity:0; transform:scale(0)">
              <ellipse cx="135" cy="155" rx="30" ry="14" fill="rgba(110,185,75,0.50)" transform="rotate(40 135 155)"/>
            </g>
            <g style="transform-origin:160px 120px; animation:leaf-unfurl 0.8s ease-out forwards 2.6s; opacity:0; transform:scale(0)">
              <ellipse cx="180" cy="120" rx="24" ry="12" fill="rgba(80,160,70,0.55)" transform="rotate(-25 180 120)"/>
            </g>
            <!-- Swaying top leaves -->
            <g style="transform-origin:160px 130px; animation:leaf-sway 3s ease-in-out infinite 3s">
              <ellipse cx="160" cy="108" rx="20" ry="10" fill="rgba(100,190,80,0.6)" transform="rotate(-10 160 108)"/>
              <ellipse cx="160" cy="108" rx="20" ry="10" fill="rgba(100,190,80,0.5)" transform="rotate(15 160 108)"/>
            </g>
            <!-- NDVI spectrum strip -->
            <defs>
              <linearGradient id="ndvi-grad" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%"   stop-color="#ff5722"/>
                <stop offset="30%"  stop-color="#ffeb3b"/>
                <stop offset="70%"  stop-color="#8bc34a"/>
                <stop offset="100%" stop-color="#1b5e20"/>
              </linearGradient>
            </defs>
            <rect x="20" y="340" width="280" height="8" rx="4" fill="url(#ndvi-grad)" style="animation:ndvi-pulse 3s ease-in-out infinite"/>
            <text x="20"  y="358" font-family="Inter,sans-serif" font-size="8" fill="rgba(255,255,255,0.4)">Low NDVI</text>
            <text x="220" y="358" font-family="Inter,sans-serif" font-size="8" fill="rgba(255,255,255,0.4)">High NDVI (healthy)</text>
          </svg>
        </div>
"""

# Social: animated network of connected nodes
SOCIAL_DECO_CSS = """
/* ── Social hero decoration ─────────────────────────────── */
.social-deco-wrap {
  position: absolute; right: 0; top: 0; bottom: 0;
  width: 340px; pointer-events: none; opacity: 0.55; overflow: hidden;
}
@keyframes node-pulse {
  0%,100% { r: 6; }
  50%      { r: 8; }
}
@keyframes link-flow {
  0%   { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: -40; }
}
@keyframes wave-out {
  0%   { r: 8;  opacity: 0.6; }
  100% { r: 55; opacity: 0; }
}
"""

# Node positions (x,y) and connections
NODES = [
    (170,130,'#7eb8d4',True,'node-pulse 2.8s ease-in-out infinite'),
    (240,85, '#7eb8d4',False,'node-pulse 3.2s ease-in-out infinite 0.5s'),
    (260,170,'#7eb8d4',False,'node-pulse 2.5s ease-in-out infinite 1s'),
    (220,240,'#7eb8d4',False,'node-pulse 3.5s ease-in-out infinite 0.2s'),
    (135,250,'#7eb8d4',False,'node-pulse 2.9s ease-in-out infinite 1.3s'),
    (80, 190,'#7eb8d4',False,'node-pulse 3.1s ease-in-out infinite 0.7s'),
    (90, 105,'#7eb8d4',False,'node-pulse 2.6s ease-in-out infinite 1.6s'),
    (185,60, '#7eb8d4',False,'node-pulse 3.4s ease-in-out infinite 0.3s'),
    (295,120,'#7eb8d4',False,'node-pulse 2.7s ease-in-out infinite 1.1s'),
    (300,230,'#7eb8d4',False,'node-pulse 3.3s ease-in-out infinite 0.8s'),
    (60, 270,'#7eb8d4',False,'node-pulse 2.4s ease-in-out infinite 1.4s'),
    (155,320,'#7eb8d4',False,'node-pulse 3.0s ease-in-out infinite 0.6s'),
]
EDGES = [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(1,7),(1,8),(2,8),(2,9),(3,9),(3,11),(4,10),(4,11),(5,6),(5,10),(6,7),(7,1)]

def social_deco_html():
    lines_svg = ''
    for a, b in EDGES:
        x1,y1 = NODES[a][0], NODES[a][1]
        x2,y2 = NODES[b][0], NODES[b][1]
        lines_svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="rgba(126,184,212,0.20)" stroke-width="1.2" stroke-dasharray="5 3" style="animation:link-flow 3s linear infinite"/>\n'

    nodes_svg = ''
    for i, (x,y,color,center,anim) in enumerate(NODES):
        if center:
            nodes_svg += f'<circle cx="{x}" cy="{y}" r="8"  fill="none" stroke="rgba(126,184,212,0.35)" stroke-width="1" style="animation:wave-out 3s ease-out infinite"/>\n'
            nodes_svg += f'<circle cx="{x}" cy="{y}" r="8"  fill="none" stroke="rgba(126,184,212,0.25)" stroke-width="1" style="animation:wave-out 3s ease-out infinite 1s"/>\n'
        nodes_svg += f'<circle cx="{x}" cy="{y}" r="6" fill="{color}" fill-opacity="0.25" stroke="{color}" stroke-width="1.5" style="animation:{anim}"/>\n'

    return f"""
        <div class="social-deco-wrap" aria-hidden="true">
          <svg viewBox="0 0 340 360" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
{lines_svg}{nodes_svg}          </svg>
        </div>
"""

# ─────────────────────────────────────────────────────────────────────
# Apply to each page
# ─────────────────────────────────────────────────────────────────────
def process_page(filename, counts, colors, label_lo, label_hi, accent,
                 deco_css, deco_html, hero_section_id='hero'):

    with open(f'outputs/{filename}', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add scroll progress bar HTML + CSS
    html = html.replace('<body>\n', '<body>\n<div id="scroll-progress"></div>\n', 1)

    SHARED_CSS = f"""
/* ── Scroll progress bar ──────────────────────────────────── */
#scroll-progress {{
  position: fixed; top: 0; left: 0; height: 3px;
  background: linear-gradient(90deg, {accent} 0%, {accent}aa 100%);
  z-index: 99999; width: 0%; pointer-events: none; transition: width 0.06s linear;
}}
{CHART_CSS}
{deco_css}
"""
    # Inject before last </style> before </head>
    html = html.replace('</style>\n</head>', SHARED_CSS + '</style>\n</head>', 1)

    # 2. Replace the bar chart block
    # Find the bar-chart div in the distribution section
    old_bar_re = r'<div class="bar-chart reveal" id="bar-chart">.*?</div>\n      </div>\n\n    </div>\n  </section>'
    new_chart = make_area_chart(counts, colors, label_lo, label_hi, accent)
    new_block  = f'{new_chart}\n      </div>\n\n    </div>\n  </section>'
    html = re.sub(old_bar_re, new_block, html, count=1, flags=re.DOTALL)

    # 3. Add decorative illustration to hero (inject into hero section)
    # Find hero section and add position:relative + deco div before hero-inner closing
    html = html.replace(
        f'  <section id="{hero_section_id}">\n',
        f'  <section id="{hero_section_id}" style="position:relative; overflow:hidden;">\n',
        1
    )
    # Inject deco before the closing </section> of hero
    # Anchor: </div>\n  </section> after hero-inner
    # We do it by finding the hero-inner close which comes before the next <section
    hero_close_old = '    </div>\n  </section>\n\n  <!-- '
    hero_close_new = deco_html + '\n    </div>\n  </section>\n\n  <!-- '
    html = html.replace(hero_close_old, hero_close_new, 1)

    # 4. Add JS before </body>
    html = html.replace('</body>', CHART_JS + '\n</body>', 1)

    with open(f'outputs/{filename}', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{filename} enhanced.')


process_page(
    'heat.html',
    HEAT_COUNTS, HEAT_COLORS,
    'Cool', 'Hottest',
    '#ff7043',
    HEAT_DECO_CSS,
    HEAT_DECO_HTML,
)

process_page(
    'green.html',
    GREEN_COUNTS, GREEN_COLORS,
    'Low deficit', 'Critical deficit',
    '#66bb6a',
    GREEN_DECO_CSS,
    GREEN_DECO_HTML,
)

process_page(
    'social.html',
    SOCIAL_COUNTS, SOCIAL_COLORS,
    'Low vulnerability', 'High vulnerability',
    '#7eb8d4',
    SOCIAL_DECO_CSS,
    social_deco_html(),
)

print('All layer pages enhanced.')
