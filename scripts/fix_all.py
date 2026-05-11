#!/usr/bin/env python3
"""
Fix all remaining issues:
  Website: AI-powered text, double dashes, nav active states, index→layer links
  Map: green colormap, sidebar redesign (professional light buttons, split sections,
       slider spacing, remove colored labels)
"""
import re

OUT = "/Users/gaelmensalopez/ugpi-barcelona/outputs"

# ═══════════════════════════════════════════════════════════
# WEBSITE FIXES
# ═══════════════════════════════════════════════════════════

# ── 1. index.html ────────────────────────────────────────
with open(f"{OUT}/index.html", "r") as f:
    idx = f.read()

# Fix hero subtitle (remove AI-powered + machine learning)
idx = idx.replace(
    "AI-powered decision support for urban planners, combining satellite imagery, machine learning and census data into one actionable priority score.",
    "Decision support for urban planners, combining satellite imagery, Copernicus data and census statistics into one actionable priority score."
)

# Fix -- in quote attribution
idx = idx.replace(
    "Research Manager, IEEC -- Institut d'Estudis Espacials de Catalunya",
    "Research Manager, IEEC, Institut d'Estudis Espacials de Catalunya"
)

# Add "Explore" links to innovation cards (after the last <p> in each card)
idx = idx.replace(
    """          <span style="font-family:'Space Grotesk',sans-serif; font-size:11px; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#ff7043;">Heat</span>
          <p style="font-size:16px; font-weight:600; color:var(--on-surface); letter-spacing:-0.01em;">Land Surface Temperature from Landsat at 30m</p>
          <p style="font-size:14px; line-height:22px; color:var(--on-surface-variant);">Previously only accessible to GIS specialists. Now surfaced as an actionable score for every census tract.</p>
        </div>""",
    """          <span style="font-family:'Space Grotesk',sans-serif; font-size:11px; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#ff7043;">Heat</span>
          <p style="font-size:16px; font-weight:600; color:var(--on-surface); letter-spacing:-0.01em;">Land Surface Temperature from Landsat at 30m</p>
          <p style="font-size:14px; line-height:22px; color:var(--on-surface-variant);">Previously only accessible to GIS specialists. Now surfaced as an actionable score for every census tract.</p>
          <a href="heat.html" style="font-size:12px; font-weight:600; color:#ff7043; text-decoration:none; display:inline-flex; align-items:center; gap:5px; margin-top:4px; opacity:0.85; transition:opacity 0.2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.85'">Explore the data <svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 10L10 2M10 2H4M10 2V8"/></svg></a>
        </div>"""
)
idx = idx.replace(
    """          <span style="font-family:'Space Grotesk',sans-serif; font-size:11px; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#a0d48d;">Green Space</span>
          <p style="font-size:16px; font-weight:600; color:var(--on-surface); letter-spacing:-0.01em;">NDVI vegetation index from Sentinel-2 at 10m</p>
          <p style="font-size:14px; line-height:22px; color:var(--on-surface-variant);">Inverted so low vegetation equals high deficit. Tells planners not just where green space exists -- but where it is missing most.</p>
        </div>""",
    """          <span style="font-family:'Space Grotesk',sans-serif; font-size:11px; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#a0d48d;">Green Space</span>
          <p style="font-size:16px; font-weight:600; color:var(--on-surface); letter-spacing:-0.01em;">NDVI vegetation index from Sentinel-2 at 10m</p>
          <p style="font-size:14px; line-height:22px; color:var(--on-surface-variant);">Inverted so low vegetation equals high deficit. Tells planners not just where green space exists, but where it is missing most.</p>
          <a href="green.html" style="font-size:12px; font-weight:600; color:#a0d48d; text-decoration:none; display:inline-flex; align-items:center; gap:5px; margin-top:4px; opacity:0.85; transition:opacity 0.2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.85'">Explore the data <svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 10L10 2M10 2H4M10 2V8"/></svg></a>
        </div>"""
)
idx = idx.replace(
    """          <span style="font-family:'Space Grotesk',sans-serif; font-size:11px; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#7eb8d4;">Social Vulnerability</span>
          <p style="font-size:16px; font-weight:600; color:var(--on-surface); letter-spacing:-0.01em;">Elderly population share plus low income index</p>
          <p style="font-size:14px; line-height:22px; color:var(--on-surface-variant);">The only existing Barcelona index to embed equity as a formal input. A vulnerable tract is structurally prioritised, not just noted.</p>
        </div>""",
    """          <span style="font-family:'Space Grotesk',sans-serif; font-size:11px; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#7eb8d4;">Social Vulnerability</span>
          <p style="font-size:16px; font-weight:600; color:var(--on-surface); letter-spacing:-0.01em;">Elderly population share plus low income index</p>
          <p style="font-size:14px; line-height:22px; color:var(--on-surface-variant);">The only existing Barcelona index to embed equity as a formal input. A vulnerable tract is structurally prioritised, not just noted.</p>
          <a href="social.html" style="font-size:12px; font-weight:600; color:#7eb8d4; text-decoration:none; display:inline-flex; align-items:center; gap:5px; margin-top:4px; opacity:0.85; transition:opacity 0.2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.85'">Explore the data <svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 10L10 2M10 2H4M10 2V8"/></svg></a>
        </div>"""
)

with open(f"{OUT}/index.html", "w") as f:
    f.write(idx)
print("index.html done")

# ── 2. Fix -- across all pages ────────────────────────────
fixes = {
    "social.html": [
        ("City mean: 21.7% -- range 4% to 41%", "City mean: 21.7% (range 4% to 41%)"),
    ],
    "validation.html": [
        ("Research Manager, IEEC -- Institut d'Estudis Espacials de Catalunya",
         "Research Manager, IEEC, Institut d'Estudis Espacials de Catalunya"),
        ("Social vulnerability is not an afterthought -- it is a formal input to the score.",
         "Social vulnerability is not an afterthought. It is a formal input to the score."),
        ("The data does not change -- the interpretation does.",
         "The data does not change. The interpretation does."),
        ("unlike fragmented departmental data systems, because it synthesises complex multi-source data into one",
         "unlike fragmented departmental data systems. It synthesises complex multi-source data into one"),
    ],
    "about.html": [
        ("three fully independent data streams -- thermal infrared satellite imagery,",
         "three fully independent data streams: thermal infrared satellite imagery,"),
        ("Perspectives on AI, Business and Data (PAIBS) -- ESADE Business School",
         "Perspectives on AI, Business and Data (PAIBS), ESADE Business School"),
        ("Summer 2023 (satellite) -- 2024 (census)",
         "Summer 2023 (satellite), 2024 (census)"),
        ("UGPI Barcelona -- Project framing question, ESADE PAIBS Group 8, 2025-2026",
         "UGPI Barcelona, ESADE PAIBS Group 8, 2025-2026"),
        ("Group 8 -- ESADE PAIBS.",
         "Group 8, ESADE PAIBS."),
        ("Research Manager, Institut d'Estudis Espacials de Catalunya (IEEC) -- Expert",
         "Research Manager, Institut d'Estudis Espacials de Catalunya (IEEC), Expert"),
        ("Expert interview -- Davoud Omarzadeh, IEEC",
         "Expert interview, Davoud Omarzadeh, IEEC"),
        ("Dec 2025 -- Feb 2026", "Dec 2025 to Feb 2026"),
        ("Apr -- May 2026",      "Apr to May 2026"),
    ],
}

for fname, replacements in fixes.items():
    with open(f"{OUT}/{fname}", "r") as f:
        text = f.read()
    for old, new in replacements:
        text = text.replace(old, new)
    with open(f"{OUT}/{fname}", "w") as f:
        f.write(text)
    print(f"{fname} done")

# ── 3. Fix nav active states on heat/green/social ────────
for fname in ["heat.html", "green.html", "social.html"]:
    with open(f"{OUT}/{fname}", "r") as f:
        text = f.read()
    # These pages shouldn't mark Methodology as active (they're sub-pages)
    text = text.replace(
        '<a href="methodology.html" class="active">Methodology</a>',
        '<a href="methodology.html">Methodology</a>'
    )
    with open(f"{OUT}/{fname}", "w") as f:
        f.write(text)
    print(f"{fname} nav fixed")


# ═══════════════════════════════════════════════════════════
# MAP REDESIGN
# ═══════════════════════════════════════════════════════════
MAP = f"{OUT}/ugpi_interactive_map.html"
with open(MAP, "r") as f:
    m = f.read()

# ── 4. Green colormap (yellow-red → sequential greens) ───
m = m.replace(
    "green:  { colors: [\"#FFFFB2\",\"#FECC5C\",\"#FD8D3C\",\"#F03B20\",\"#BD0026\"],         vmin:1, vmax:10 },",
    "green:  { colors: [\"#edf8e9\",\"#bae4b3\",\"#74c476\",\"#31a354\",\"#006d2c\"],         vmin:1, vmax:10 },"
)
m = m.replace(
    "green:  { label: \"Green Space Deficit Score\",  gradient: \"linear-gradient(to right,#FFFFB2,#FECC5C,#FD8D3C,#F03B20,#BD0026)\",                 lo: \"1 - Low deficit\",       hi: \"10 - High deficit\" },",
    "green:  { label: \"Green Space Deficit Score\",  gradient: \"linear-gradient(to right,#edf8e9,#bae4b3,#74c476,#31a354,#006d2c)\",                 lo: \"1 - Low deficit\",       hi: \"10 - Critical deficit\" },"
)

# ── 5. Replace left sidebar "Data Layers" section ────────
OLD_DATA_LAYERS = """\
        <!-- Data Layers -->
        <div style="border-top:1px solid rgba(255,255,255,0.10); padding-top:12px; margin-top:12px; margin-bottom:0;">
            <div style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#7eb8d4; margin-bottom:9px;">Data Layers</div>
            <div style="font-size:11.5px; margin-bottom:6px; display:flex; align-items:center; gap:9px;">
                <span style="width:8px;height:8px;border-radius:50%;background:#F03B20;flex-shrink:0;display:inline-block;"></span>
                <span><strong style="color:#f0a080; font-weight:600;">Heat</strong> <span style="color:#5a7898;">Land Surface Temperature</span></span>
            </div>
            <div style="font-size:11.5px; margin-bottom:6px; display:flex; align-items:center; gap:9px;">
                <span style="width:8px;height:8px;border-radius:50%;background:#56a85e;flex-shrink:0;display:inline-block;"></span>
                <span><strong style="color:#80c080; font-weight:600;">Green Space Deficit</strong> <span style="color:#5a7898;">NDVI gap</span></span>
            </div>
            <div style="font-size:11.5px; display:flex; align-items:center; gap:9px;">
                <span style="width:8px;height:8px;border-radius:50%;background:#7b9fd4;flex-shrink:0;display:inline-block;"></span>
                <span><strong style="color:#9ab4e0; font-weight:600;">Social Vulnerability</strong> <span style="color:#5a7898;">Elderly + income</span></span>
            </div>
            <div style="margin-top:7px; font-size:10px; color:#3d5268; letter-spacing:0.01em;">
                Equal-weight composite &middot; Summer 2023
            </div>
        </div>"""

NEW_DATA_LAYERS = """\
        <!-- Data Layers -->
        <div style="border-top:1px solid rgba(255,255,255,0.10); padding-top:12px; margin-top:12px; margin-bottom:0;">
            <div style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:rgba(255,255,255,0.30); margin-bottom:9px;">Data Layers</div>
            <div style="display:flex; flex-direction:column; gap:6px;">
                <div style="display:flex; align-items:center; gap:9px;">
                    <span style="width:6px;height:6px;border-radius:50%;background:rgba(240,160,128,0.55);flex-shrink:0;display:inline-block;"></span>
                    <span style="font-size:11px; color:rgba(255,255,255,0.65); font-weight:500;">Heat <span style="color:rgba(255,255,255,0.28); font-weight:400;">· Land Surface Temperature</span></span>
                </div>
                <div style="display:flex; align-items:center; gap:9px;">
                    <span style="width:6px;height:6px;border-radius:50%;background:rgba(86,168,94,0.55);flex-shrink:0;display:inline-block;"></span>
                    <span style="font-size:11px; color:rgba(255,255,255,0.65); font-weight:500;">Green Space Deficit <span style="color:rgba(255,255,255,0.28); font-weight:400;">· NDVI</span></span>
                </div>
                <div style="display:flex; align-items:center; gap:9px;">
                    <span style="width:6px;height:6px;border-radius:50%;background:rgba(123,159,212,0.55);flex-shrink:0;display:inline-block;"></span>
                    <span style="font-size:11px; color:rgba(255,255,255,0.65); font-weight:500;">Social Vulnerability <span style="color:rgba(255,255,255,0.28); font-weight:400;">· Elderly + income</span></span>
                </div>
            </div>
            <div style="margin-top:8px; font-size:9.5px; color:rgba(255,255,255,0.18); letter-spacing:0.01em;">
                Equal-weight composite &middot; Summer 2023
            </div>
        </div>"""

assert OLD_DATA_LAYERS in m, "Data Layers section not found"
m = m.replace(OLD_DATA_LAYERS, NEW_DATA_LAYERS, 1)

# ── 6. Replace View Layer section (split into layers + tools) ──
OLD_VIEW_LAYER = """\
        <!-- View Layer -->
        <div style="border-top:1px solid rgba(255,255,255,0.10); padding-top:12px; margin-top:12px;">
            <div style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#7eb8d4; margin-bottom:9px;">View Layer</div>
            <div style="display:flex; flex-direction:column; gap:4px;">
                <button id="btn-ugpi"   onclick="switchLayer('ugpi')"   style="background:rgba(126,184,212,0.20);color:#e8edf3;border:1px solid rgba(126,184,212,0.45);padding:7px 12px;border-radius:5px;cursor:pointer;font-family:'Inter','Segoe UI',Arial,sans-serif;font-size:11.5px;text-align:left;transition:all 0.15s;letter-spacing:0.01em;">UGPI Combined</button>
                <button id="btn-heat"   onclick="switchLayer('heat')"   style="background:rgba(255,255,255,0.05);color:#a0b8cc;border:1px solid rgba(255,255,255,0.09);padding:7px 12px;border-radius:5px;cursor:pointer;font-family:'Inter','Segoe UI',Arial,sans-serif;font-size:11.5px;text-align:left;transition:all 0.15s;">Heat</button>
                <button id="btn-green"  onclick="switchLayer('green')"  style="background:rgba(255,255,255,0.05);color:#a0b8cc;border:1px solid rgba(255,255,255,0.09);padding:7px 12px;border-radius:5px;cursor:pointer;font-family:'Inter','Segoe UI',Arial,sans-serif;font-size:11.5px;text-align:left;transition:all 0.15s;">Green Space Deficit</button>
                <button id="btn-social" onclick="switchLayer('social')" style="background:rgba(255,255,255,0.05);color:#a0b8cc;border:1px solid rgba(255,255,255,0.09);padding:7px 12px;border-radius:5px;cursor:pointer;font-family:'Inter','Segoe UI',Arial,sans-serif;font-size:11.5px;text-align:left;transition:all 0.15s;">Social Vulnerability</button>
            </div>
            <div style="margin-top:5px; display:flex; flex-direction:column; gap:4px;">
                <button id="btn-district" onclick="toggleDistrictView()" style="background:rgba(255,255,255,0.05);color:#a0b8cc;border:1px solid rgba(255,255,255,0.09);padding:7px 12px;border-radius:5px;cursor:pointer;font-family:'Inter','Segoe UI',Arial,sans-serif;font-size:11.5px;text-align:left;transition:all 0.15s;width:100%;">District View</button>
                <button id="btn-compare" onclick="toggleCompareMode()" style="background:rgba(255,255,255,0.05);color:#a0b8cc;border:1px solid rgba(255,255,255,0.09);padding:7px 12px;border-radius:5px;cursor:pointer;font-family:'Inter','Segoe UI',Arial,sans-serif;font-size:11.5px;text-align:left;transition:all 0.15s;width:100%;">Compare Tracts</button>
                <button id="btn-sim" onclick="toggleSimMode()" style="background:rgba(255,255,255,0.05);color:#a0b8cc;border:1px solid rgba(255,255,255,0.09);padding:7px 12px;border-radius:5px;cursor:pointer;font-family:'Inter','Segoe UI',Arial,sans-serif;font-size:11.5px;text-align:left;transition:all 0.15s;width:100%;">Simulate Intervention</button>
            </div>
        </div>"""

NEW_VIEW_LAYER = """\
        <!-- Map Layer selection -->
        <div style="border-top:1px solid rgba(255,255,255,0.10); padding-top:12px; margin-top:12px;">
            <div style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:rgba(255,255,255,0.30); margin-bottom:8px;">Map Layer</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px;">
                <button id="btn-ugpi"   onclick="switchLayer('ugpi')"   style="background:rgba(255,255,255,0.88);color:#1b2838;border:1px solid transparent;padding:9px 8px;border-radius:6px;cursor:pointer;font-family:'Inter','Segoe UI',Arial,sans-serif;font-size:11px;font-weight:600;text-align:center;transition:all 0.15s;letter-spacing:0.01em;">UGPI</button>
                <button id="btn-heat"   onclick="switchLayer('heat')"   style="background:rgba(255,255,255,0.05);color:rgba(255,255,255,0.45);border:1px solid rgba(255,255,255,0.08);padding:9px 8px;border-radius:6px;cursor:pointer;font-family:'Inter','Segoe UI',Arial,sans-serif;font-size:11px;font-weight:400;text-align:center;transition:all 0.15s;">Heat</button>
                <button id="btn-green"  onclick="switchLayer('green')"  style="background:rgba(255,255,255,0.05);color:rgba(255,255,255,0.45);border:1px solid rgba(255,255,255,0.08);padding:9px 8px;border-radius:6px;cursor:pointer;font-family:'Inter','Segoe UI',Arial,sans-serif;font-size:11px;font-weight:400;text-align:center;transition:all 0.15s;">Green Deficit</button>
                <button id="btn-social" onclick="switchLayer('social')" style="background:rgba(255,255,255,0.05);color:rgba(255,255,255,0.45);border:1px solid rgba(255,255,255,0.08);padding:9px 8px;border-radius:6px;cursor:pointer;font-family:'Inter','Segoe UI',Arial,sans-serif;font-size:11px;font-weight:400;text-align:center;transition:all 0.15s;">Social Vuln.</button>
            </div>
        </div>

        <!-- Analysis Tools -->
        <div style="border-top:1px solid rgba(255,255,255,0.08); padding-top:10px; margin-top:10px;">
            <div style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:rgba(255,255,255,0.30); margin-bottom:8px;">Analysis Tools</div>
            <div style="display:flex; flex-direction:column; gap:4px;">
                <button id="btn-district" onclick="toggleDistrictView()" style="background:transparent;color:rgba(255,255,255,0.45);border:1px solid rgba(255,255,255,0.07);padding:8px 12px;border-radius:5px;cursor:pointer;font-family:'Inter','Segoe UI',Arial,sans-serif;font-size:11px;font-weight:400;text-align:left;transition:all 0.15s;width:100%;">District View</button>
                <button id="btn-compare" onclick="toggleCompareMode()" style="background:transparent;color:rgba(255,255,255,0.45);border:1px solid rgba(255,255,255,0.07);padding:8px 12px;border-radius:5px;cursor:pointer;font-family:'Inter','Segoe UI',Arial,sans-serif;font-size:11px;font-weight:400;text-align:left;transition:all 0.15s;width:100%;">Compare Tracts</button>
                <button id="btn-sim" onclick="toggleSimMode()" style="background:transparent;color:rgba(255,255,255,0.45);border:1px solid rgba(255,255,255,0.07);padding:8px 12px;border-radius:5px;cursor:pointer;font-family:'Inter','Segoe UI',Arial,sans-serif;font-size:11px;font-weight:400;text-align:left;transition:all 0.15s;width:100%;">Simulate Intervention</button>
            </div>
        </div>"""

assert OLD_VIEW_LAYER in m, "View Layer section not found"
m = m.replace(OLD_VIEW_LAYER, NEW_VIEW_LAYER, 1)

# ── 7. Fix weight slider spacing ─────────────────────────
# Change margin-bottom:8px → 14px on each slider group
m = m.replace(
    "            <div style=\"margin-bottom:8px;\">\n                <div style=\"display:flex; justify-content:space-between; font-size:11px; margin-bottom:3px;\">\n                    <span style=\"color:#f0a080;",
    "            <div style=\"margin-bottom:16px;\">\n                <div style=\"display:flex; justify-content:space-between; font-size:11px; margin-bottom:4px;\">\n                    <span style=\"color:#f0a080;"
)
m = m.replace(
    "            <div style=\"margin-bottom:8px;\">\n                <div style=\"display:flex; justify-content:space-between; font-size:11px; margin-bottom:3px;\">\n                    <span style=\"color:#80c080;",
    "            <div style=\"margin-bottom:16px;\">\n                <div style=\"display:flex; justify-content:space-between; font-size:11px; margin-bottom:4px;\">\n                    <span style=\"color:#80c080;"
)
m = m.replace(
    "            <div style=\"margin-bottom:8px;\">\n                <div style=\"display:flex; justify-content:space-between; font-size:11px; margin-bottom:3px;\">\n                    <span style=\"color:#9ab4e0;",
    "            <div style=\"margin-bottom:8px;\">\n                <div style=\"display:flex; justify-content:space-between; font-size:11px; margin-bottom:4px;\">\n                    <span style=\"color:#9ab4e0;"
)

# ── 8. Update JS button state functions ──────────────────
m = m.replace(
    """  function _setLayerBtnState(activeKey) {
    ['ugpi','heat','green','social'].forEach(function(k) {
      var btn = document.getElementById('btn-' + k);
      if (!btn) return;
      var on = (k === activeKey);
      btn.style.background  = on ? 'rgba(126,184,212,0.25)' : 'rgba(255,255,255,0.07)';
      btn.style.color       = on ? '#e8edf3'                : '#a0b8cc';
      btn.style.borderColor = on ? '#7eb8d4'                : 'rgba(255,255,255,0.12)';
    });
  }""",
    """  function _setLayerBtnState(activeKey) {
    ['ugpi','heat','green','social'].forEach(function(k) {
      var btn = document.getElementById('btn-' + k);
      if (!btn) return;
      var on = (k === activeKey);
      btn.style.background  = on ? 'rgba(255,255,255,0.88)' : 'rgba(255,255,255,0.05)';
      btn.style.color       = on ? '#1b2838'                : 'rgba(255,255,255,0.45)';
      btn.style.borderColor = on ? 'transparent'            : 'rgba(255,255,255,0.08)';
      btn.style.fontWeight  = on ? '600'                    : '400';
    });
  }"""
)

m = m.replace(
    """  function _setDistrictBtnState(active) {
    var btn = document.getElementById('btn-district');
    if (!btn) return;
    btn.style.background  = active ? 'rgba(126,184,212,0.25)' : 'rgba(255,255,255,0.07)';
    btn.style.color       = active ? '#e8edf3'                : '#a0b8cc';
    btn.style.borderColor = active ? '#7eb8d4'                : 'rgba(255,255,255,0.12)';
  }""",
    """  function _setDistrictBtnState(active) {
    var btn = document.getElementById('btn-district');
    if (!btn) return;
    btn.style.background  = active ? 'rgba(126,184,212,0.14)' : 'transparent';
    btn.style.color       = active ? '#7eb8d4'                : 'rgba(255,255,255,0.45)';
    btn.style.borderColor = active ? 'rgba(126,184,212,0.35)' : 'rgba(255,255,255,0.07)';
    btn.style.fontWeight  = active ? '600'                    : '400';
  }"""
)

m = m.replace(
    """  function _setCompareBtnState(active) {
    var btn = document.getElementById('btn-compare');
    if (!btn) return;
    btn.style.background  = active ? 'rgba(254,204,92,0.20)' : 'rgba(255,255,255,0.07)';
    btn.style.color       = active ? '#fecc5c'               : '#a0b8cc';
    btn.style.borderColor = active ? '#fecc5c'               : 'rgba(255,255,255,0.12)';
  }""",
    """  function _setCompareBtnState(active) {
    var btn = document.getElementById('btn-compare');
    if (!btn) return;
    btn.style.background  = active ? 'rgba(254,204,92,0.14)'  : 'transparent';
    btn.style.color       = active ? '#fecc5c'                : 'rgba(255,255,255,0.45)';
    btn.style.borderColor = active ? 'rgba(254,204,92,0.35)'  : 'rgba(255,255,255,0.07)';
    btn.style.fontWeight  = active ? '600'                    : '400';
  }"""
)

m = m.replace(
    """  function _setSimBtnState(active) {
    var btn = document.getElementById('btn-sim');
    if (!btn) return;
    btn.style.background  = active ? 'rgba(86,168,94,0.20)'  : 'rgba(255,255,255,0.07)';
    btn.style.color       = active ? '#80c080'               : '#a0b8cc';
    btn.style.borderColor = active ? '#56a85e'               : 'rgba(255,255,255,0.12)';
  }""",
    """  function _setSimBtnState(active) {
    var btn = document.getElementById('btn-sim');
    if (!btn) return;
    btn.style.background  = active ? 'rgba(86,168,94,0.14)'   : 'transparent';
    btn.style.color       = active ? '#80c080'                : 'rgba(255,255,255,0.45)';
    btn.style.borderColor = active ? 'rgba(86,168,94,0.35)'   : 'rgba(255,255,255,0.07)';
    btn.style.fontWeight  = active ? '600'                    : '400';
  }"""
)

# ── 9. Adjust Weights section label styling ──────────────
m = m.replace(
    '            <div style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#7eb8d4; margin-bottom:9px;">Adjust Weights</div>',
    '            <div style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:rgba(255,255,255,0.30); margin-bottom:10px;">Adjust Weights</div>'
)
m = m.replace(
    '            <div style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#7eb8d4; margin-bottom:9px;">Priority Filter</div>',
    '            <div style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:rgba(255,255,255,0.30); margin-bottom:9px;">Priority Filter</div>'
)

with open(MAP, "w") as f:
    f.write(m)
print("ugpi_interactive_map.html done")

print("\nAll fixes applied successfully.")
