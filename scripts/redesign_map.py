#!/usr/bin/env python3
"""
Redesign ugpi_interactive_map.html:
- Full-height left sidebar (flush left, 300px wide)
- Full-height right sidebar (flush right, 280px wide)
- Map fills middle space between sidebars
- No emojis anywhere
- Radar/spider chart in tract popup (Chart.js)
- District ranking table in right sidebar
- Inter font, professional styling
"""

import re

SRC = "/Users/gaelmensalopez/ugpi-barcelona/outputs/ugpi_interactive_map.html"

with open(SRC, "r", encoding="utf-8") as f:
    content = f.read()

# ─────────────────────────────────────────────────────────────
# 1. Add Chart.js + Inter font to <head>
# ─────────────────────────────────────────────────────────────
LAST_CDN = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css"/>'
NEW_CDNS = (
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css"/>\n'
    '    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>\n'
    '    <link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
)
assert LAST_CDN in content, "CDN anchor not found"
content = content.replace(LAST_CDN, NEW_CDNS, 1)

# ─────────────────────────────────────────────────────────────
# 2. Fix map div CSS to be sidebar-aware
# ─────────────────────────────────────────────────────────────
OLD_MAP_CSS = """                #map_fc544ffef9933d660d25525d9493f89e {
                    position: relative;
                    width: 100.0%;
                    height: 100.0%;
                    left: 0.0%;
                    top: 0.0%;
                }"""
NEW_MAP_CSS = """                #map_fc544ffef9933d660d25525d9493f89e {
                    position: absolute;
                    top: 0;
                    bottom: 0;
                    left: 300px;
                    right: 280px;
                    width: auto;
                    height: 100%;
                }"""
assert OLD_MAP_CSS in content, "Map CSS anchor not found"
content = content.replace(OLD_MAP_CSS, NEW_MAP_CSS, 1)

# ─────────────────────────────────────────────────────────────
# 3. Replace search container + left panel with new left sidebar
#    (original lines ~95–322)
# ─────────────────────────────────────────────────────────────
OLD_SEARCH_START = '<div style="\n    position: fixed;\n    top: 10px;\n    left: 50%;'
OLD_LEFT_END     = '</div>\n    \n<div style="\n    position: fixed;\n    bottom: 34px;\n    right: 10px;'

# Find the section to replace
search_idx = content.find(OLD_SEARCH_START)
legend_idx = content.find('<div style="\n    position: fixed;\n    bottom: 34px;\n    right: 10px;')
assert search_idx != -1, "Search container start not found"
assert legend_idx != -1, "Legend start not found"

OLD_LEFT_SECTION = content[search_idx:legend_idx]

NEW_LEFT_SIDEBAR = '''\
<div id="left-sidebar" style="
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: 300px;
    z-index: 9999;
    background: #1b2838;
    border-right: 1px solid rgba(255,255,255,0.10);
    display: flex;
    flex-direction: column;
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    overflow: hidden;
    pointer-events: auto;
">
    <!-- Header -->
    <div style="padding:20px 20px 0; flex-shrink:0;">
        <div style="font-size:13.5px; font-weight:700; letter-spacing:0.01em; color:#ffffff; line-height:1.3; margin-bottom:3px;">
            Urban Greening Priority Index
        </div>
        <div style="font-size:10.5px; color:#4a6580; margin-bottom:14px; line-height:1.4; letter-spacing:0.01em;">
            Barcelona &middot; Decision Support Tool
        </div>
        <div style="height:1px; background:rgba(255,255,255,0.10); margin-bottom:0;"></div>
    </div>

    <!-- Search -->
    <div style="padding:12px 16px 0; flex-shrink:0;">
        <div id="search-container" style="position:relative;">
            <div style="
                display:flex; align-items:center;
                background:rgba(255,255,255,0.06);
                border:1px solid rgba(255,255,255,0.12);
                border-radius:6px;
                padding:0 8px 0 10px;
                gap:6px;
                transition:border-color 0.15s;
            ">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#4a6580" stroke-width="2.5" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                <input
                    id="search-input"
                    type="text"
                    placeholder="Search address..."
                    autocomplete="off"
                    onkeydown="if(event.key===\'Enter\'){searchAddress();}else if(event.key===\'Escape\'){clearSearch();}"
                    oninput="onSearchInput()"
                    onblur="setTimeout(function(){hideSearchDropdown()},160)"
                    style="
                        flex:1; background:transparent; border:none; outline:none;
                        color:#e8edf3; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;
                        font-size:11.5px; padding:8px 2px; min-width:0;
                    "
                >
                <button
                    id="search-clear"
                    onclick="clearSearch()"
                    title="Clear"
                    style="display:none;align-items:center;justify-content:center;background:none;border:none;color:#6b829e;cursor:pointer;font-size:12px;padding:2px 4px;line-height:1;flex-shrink:0;transition:color 0.15s;"
                    onmouseover="this.style.color=\'#e8edf3\'" onmouseout="this.style.color=\'#6b829e\'"
                >&#x2715;</button>
            </div>
            <ul id="search-dropdown" style="
                display:none; position:absolute; top:calc(100% + 4px); left:0; right:0;
                background:#1b2838; border:1px solid rgba(255,255,255,0.15);
                border-radius:7px; box-shadow:0 8px 28px rgba(0,0,0,0.55);
                list-style:none; margin:0; padding:4px 0; overflow:hidden; z-index:10001;
            "></ul>
        </div>
    </div>

    <!-- Scrollable content -->
    <div style="flex:1; overflow-y:auto; padding:0 16px 8px; min-height:0;">

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
        </div>

        <!-- View Layer -->
        <div style="border-top:1px solid rgba(255,255,255,0.10); padding-top:12px; margin-top:12px;">
            <div style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#7eb8d4; margin-bottom:9px;">View Layer</div>
            <div style="display:flex; flex-direction:column; gap:4px;">
                <button id="btn-ugpi"   onclick="switchLayer(\'ugpi\')"   style="background:rgba(126,184,212,0.20);color:#e8edf3;border:1px solid rgba(126,184,212,0.45);padding:7px 12px;border-radius:5px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11.5px;text-align:left;transition:all 0.15s;letter-spacing:0.01em;">UGPI Combined</button>
                <button id="btn-heat"   onclick="switchLayer(\'heat\')"   style="background:rgba(255,255,255,0.05);color:#a0b8cc;border:1px solid rgba(255,255,255,0.09);padding:7px 12px;border-radius:5px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11.5px;text-align:left;transition:all 0.15s;">Heat</button>
                <button id="btn-green"  onclick="switchLayer(\'green\')"  style="background:rgba(255,255,255,0.05);color:#a0b8cc;border:1px solid rgba(255,255,255,0.09);padding:7px 12px;border-radius:5px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11.5px;text-align:left;transition:all 0.15s;">Green Space Deficit</button>
                <button id="btn-social" onclick="switchLayer(\'social\')" style="background:rgba(255,255,255,0.05);color:#a0b8cc;border:1px solid rgba(255,255,255,0.09);padding:7px 12px;border-radius:5px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11.5px;text-align:left;transition:all 0.15s;">Social Vulnerability</button>
            </div>
            <div style="margin-top:5px; display:flex; flex-direction:column; gap:4px;">
                <button id="btn-district" onclick="toggleDistrictView()" style="background:rgba(255,255,255,0.05);color:#a0b8cc;border:1px solid rgba(255,255,255,0.09);padding:7px 12px;border-radius:5px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11.5px;text-align:left;transition:all 0.15s;width:100%;">District View</button>
                <button id="btn-compare" onclick="toggleCompareMode()" style="background:rgba(255,255,255,0.05);color:#a0b8cc;border:1px solid rgba(255,255,255,0.09);padding:7px 12px;border-radius:5px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11.5px;text-align:left;transition:all 0.15s;width:100%;">Compare Tracts</button>
                <button id="btn-sim" onclick="toggleSimMode()" style="background:rgba(255,255,255,0.05);color:#a0b8cc;border:1px solid rgba(255,255,255,0.09);padding:7px 12px;border-radius:5px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11.5px;text-align:left;transition:all 0.15s;width:100%;">Simulate Intervention</button>
            </div>
        </div>

        <!-- Adjust Weights -->
        <div id="weight-section" style="border-top:1px solid rgba(255,255,255,0.10); padding-top:12px; margin-top:12px;">
            <div style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#7eb8d4; margin-bottom:9px;">Adjust Weights</div>
            <div style="margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:3px;">
                    <span style="color:#f0a080; font-weight:600;">Heat</span>
                    <span id="val-heat" style="color:#e8edf3;">33%</span>
                </div>
                <input type="range" id="slider-heat" min="0" max="100" value="33" oninput="onWeightSlider(\'heat\')" style="width:100%; accent-color:#f0a080; cursor:pointer; display:block;">
            </div>
            <div style="margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:3px;">
                    <span style="color:#80c080; font-weight:600;">Green Space</span>
                    <span id="val-green" style="color:#e8edf3;">33%</span>
                </div>
                <input type="range" id="slider-green" min="0" max="100" value="33" oninput="onWeightSlider(\'green\')" style="width:100%; accent-color:#56a85e; cursor:pointer; display:block;">
            </div>
            <div style="margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:3px;">
                    <span style="color:#9ab4e0; font-weight:600;">Social Vulnerability</span>
                    <span id="val-social" style="color:#e8edf3;">34%</span>
                </div>
                <input type="range" id="slider-social" min="0" max="100" value="34" oninput="onWeightSlider(\'social\')" style="width:100%; accent-color:#7b9fd4; cursor:pointer; display:block;">
            </div>
            <div id="weight-summary" style="font-size:10px; color:#3d5268; text-align:center; margin-bottom:8px;">Heat 33% &middot; Green 33% &middot; Social 34%</div>
            <div style="display:flex; gap:6px;">
                <button onclick="resetWeights()" style="flex:0 0 auto; background:rgba(255,255,255,0.05); color:#a0b8cc; border:1px solid rgba(255,255,255,0.09); padding:7px 11px; border-radius:5px; cursor:pointer; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif; font-size:11.5px; font-weight:600; transition:background 0.15s;">Reset</button>
                <button id="btn-recalculate" onclick="recalculateUGPI()" style="flex:1; background:rgba(126,184,212,0.12); color:#e8edf3; border:1px solid rgba(126,184,212,0.35); padding:7px 12px; border-radius:5px; cursor:pointer; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif; font-size:11.5px; font-weight:600; transition:background 0.15s; letter-spacing:0.01em;">Recalculate</button>
            </div>
        </div>

        <!-- Priority Filter -->
        <div style="border-top:1px solid rgba(255,255,255,0.10); padding-top:12px; margin-top:12px; margin-bottom:12px;">
            <div style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#7eb8d4; margin-bottom:9px;">Priority Filter</div>
            <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:4px;">
                <span style="color:#c8d6e5;">Show tracts with UGPI &ge;</span>
                <span id="filter-val" style="color:#e8edf3; font-weight:600;">1.0</span>
            </div>
            <input type="range" id="slider-filter" min="1" max="10" step="0.1" value="1"
                   oninput="onFilterSlider()"
                   style="width:100%; accent-color:#7eb8d4; cursor:pointer; display:block; margin-bottom:7px;">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:6px;">
                <span id="filter-counter" style="font-size:10px; color:#3d5268;">1068 of 1068 tracts above threshold</span>
                <button onclick="resetFilter()" style="flex:0 0 auto; background:rgba(255,255,255,0.05); color:#a0b8cc; border:1px solid rgba(255,255,255,0.09); padding:3px 9px; border-radius:5px; cursor:pointer; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif; font-size:11px; font-weight:600; white-space:nowrap; transition:background 0.15s;">Show All</button>
            </div>
        </div>

    </div><!-- end scrollable content -->

    <!-- Bottom actions -->
    <div style="padding:10px 16px 14px; border-top:1px solid rgba(255,255,255,0.10); flex-shrink:0; display:flex; gap:6px;">
        <button onclick="exportCSV()" style="
            flex:1; background:rgba(255,255,255,0.05); color:#a0b8cc;
            border:1px solid rgba(255,255,255,0.09); border-radius:5px;
            padding:8px 10px; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;
            font-size:11.5px; font-weight:600; cursor:pointer;
            transition:background 0.15s; white-space:nowrap;
        " onmouseover="this.style.background=\'rgba(255,255,255,0.10)\'" onmouseout="this.style.background=\'rgba(255,255,255,0.05)\'">
            Export CSV
        </button>
        <button onclick="openWelcomeModal()" id="btn-how-to-use" style="
            flex:1; background:rgba(126,184,212,0.07); color:#7eb8d4;
            border:1px solid rgba(126,184,212,0.22); border-radius:5px;
            padding:8px 10px; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;
            font-size:11.5px; font-weight:600; cursor:pointer;
            transition:background 0.15s; white-space:nowrap;
        " onmouseover="this.style.background=\'rgba(126,184,212,0.14)\'" onmouseout="this.style.background=\'rgba(126,184,212,0.07)\'">
            How to Use
        </button>
    </div>

</div>

'''

content = content.replace(OLD_LEFT_SECTION, NEW_LEFT_SIDEBAR, 1)

# ─────────────────────────────────────────────────────────────
# 4. Replace legend panel + top20 container with right sidebar
#    (original lines ~324–404)
#    The sim/compare panels remain floating overlays
# ─────────────────────────────────────────────────────────────
OLD_LEGEND_START = '<div style="\n    position: fixed;\n    bottom: 34px;\n    right: 10px;\n    z-index: 9999;\n    background: #1b2838;\n    color: #e8edf3;\n    border-radius: 10px;\n    padding: 14px 18px 12px;\n    width: 256px;\n    box-shadow: 0 4px 18px rgba(0,0,0,0.45);\n    font-family: \'Segoe UI\', Arial, sans-serif;\n    pointer-events: none;\n">'

OLD_TOP20_CONTAINER_END = '</div>\n</div>\n    \n    \n'
# Top20 container ends just before <div id="sim-panel"
top20_end_idx = content.find('\n<div id="sim-panel"')
legend_start_idx = content.find(OLD_LEGEND_START)

assert legend_start_idx != -1, "Legend start not found"
assert top20_end_idx != -1, "Top20 end (sim-panel) not found"

OLD_LEGEND_TOP20 = content[legend_start_idx:top20_end_idx]

NEW_RIGHT_SIDEBAR = '''\

<div id="right-sidebar" style="
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    width: 280px;
    z-index: 9999;
    background: #1b2838;
    border-left: 1px solid rgba(255,255,255,0.10);
    display: flex;
    flex-direction: column;
    font-family: \'Inter\', \'Segoe UI\', Arial, sans-serif;
    overflow: hidden;
">

    <!-- Legend -->
    <div style="padding:18px 18px 14px; flex-shrink:0; border-bottom:1px solid rgba(255,255,255,0.10);">
        <div id="legend-label" style="
            font-size:9px; font-weight:700; text-transform:uppercase;
            letter-spacing:0.13em; color:#7eb8d4; margin-bottom:10px;
        ">UGPI Score</div>
        <div id="legend-bar" style="
            height:10px; border-radius:3px; margin-bottom:7px;
            background: linear-gradient(to right, #FFFFB2, #FECC5C, #FD8D3C, #F03B20, #BD0026);
        "></div>
        <div style="display:flex; justify-content:space-between; font-size:10px; color:#4a6580;">
            <span id="legend-lo">1 - Low priority</span>
            <span id="legend-hi">10 - Highest priority</span>
        </div>
    </div>

    <!-- District Rankings -->
    <div style="padding:14px 18px 10px; flex-shrink:0; border-bottom:1px solid rgba(255,255,255,0.10);">
        <div style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#7eb8d4; margin-bottom:9px;">District Rankings</div>
        <div id="district-ranking-list" style="display:flex; flex-direction:column; gap:0;">
            <!-- Populated by buildDistrictRanking() -->
        </div>
    </div>

    <!-- Top 20 Priority Tracts -->
    <div style="padding:14px 18px 0; flex:1; min-height:0; display:flex; flex-direction:column; overflow:hidden;">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:9px; flex-shrink:0;">
            <span id="top20-header-label" style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#7eb8d4;">Top 20 &middot; UGPI</span>
            <button id="top20-sort-btn" onclick="toggleTop20Sort()" style="font-size:10px; font-weight:600; color:#7eb8d4; background:transparent; border:1px solid rgba(126,184,212,0.28); border-radius:4px; padding:2px 6px; cursor:pointer; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif; white-space:nowrap; transition:all 0.15s;">High first</button>
        </div>
        <div style="display:flex; font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#2d4055; padding:3px 2px 5px; border-bottom:1px solid rgba(255,255,255,0.07); margin-bottom:3px; flex-shrink:0;">
            <span style="min-width:22px;">#</span>
            <span style="flex:1; padding-left:2px;">Tract</span>
            <span>Score</span>
        </div>
        <div id="top20-list" style="overflow-y:auto; flex:1; padding-bottom:6px;"></div>
        <div id="top20-panel" style="display:none;"></div>
    </div>

    <!-- Attribution -->
    <div style="padding:7px 18px 10px; border-top:1px solid rgba(255,255,255,0.06); flex-shrink:0;">
        <div style="font-size:9px; color:#2d4055; line-height:1.5; letter-spacing:0.01em;">
            Sentinel-2 &middot; Landsat &middot; Summer 2023 &middot; 1,068 tracts
        </div>
    </div>

</div>
'''

content = content.replace(OLD_LEGEND_TOP20, NEW_RIGHT_SIDEBAR, 1)

# ─────────────────────────────────────────────────────────────
# 5. Fix sim panel position: left:260px -> left:310px
# ─────────────────────────────────────────────────────────────
OLD_SIM_POS = '''<div id="sim-panel" style="
    position: fixed;
    top: 10px;
    left: 260px;
    z-index: 10000;
    display: none;
    background: #1b2838;
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 12px;
    box-shadow: 0 8px 36px rgba(0,0,0,0.65);
    padding: 16px 18px 14px;
    width: 310px;
    max-height: calc(100vh - 30px);
    overflow-y: auto;
    font-family: \'Segoe UI\', Arial, sans-serif;
">'''
NEW_SIM_POS = '''<div id="sim-panel" style="
    position: fixed;
    top: 10px;
    left: 310px;
    z-index: 10000;
    display: none;
    background: #1b2838;
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 10px;
    box-shadow: 0 8px 36px rgba(0,0,0,0.65);
    padding: 16px 18px 14px;
    width: 310px;
    max-height: calc(100vh - 30px);
    overflow-y: auto;
    font-family: \'Inter\', \'Segoe UI\', Arial, sans-serif;
">'''
assert OLD_SIM_POS in content, "Sim panel CSS not found"
content = content.replace(OLD_SIM_POS, NEW_SIM_POS, 1)

# ─────────────────────────────────────────────────────────────
# 6. Fix compare panel position: left:260px -> left:310px
# ─────────────────────────────────────────────────────────────
OLD_COMPARE_POS = '''<div id="compare-panel" style="
    position: fixed;
    bottom: 0px;
    left: 260px;
    z-index: 10000;
    display: none;
    background: #1b2838;
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 12px;
    box-shadow: 0 8px 36px rgba(0,0,0,0.65);
    padding: 16px 20px 14px;
    width: 520px;
    font-family: \'Segoe UI\', Arial, sans-serif;
">'''
NEW_COMPARE_POS = '''<div id="compare-panel" style="
    position: fixed;
    bottom: 10px;
    left: 310px;
    right: 290px;
    z-index: 10000;
    display: none;
    background: #1b2838;
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 10px;
    box-shadow: 0 8px 36px rgba(0,0,0,0.65);
    padding: 16px 20px 14px;
    max-width: 640px;
    font-family: \'Inter\', \'Segoe UI\', Arial, sans-serif;
">'''
assert OLD_COMPARE_POS in content, "Compare panel CSS not found"
content = content.replace(OLD_COMPARE_POS, NEW_COMPARE_POS, 1)

# ─────────────────────────────────────────────────────────────
# 7. Remove the old attribution div (now inside right sidebar)
# ─────────────────────────────────────────────────────────────
OLD_ATTR = '''\n<div style="
    position: fixed;
    bottom: 0px;
    left: 260px;
    z-index: 9999;
    background: rgba(255,255,255,0.65);
    color: #505050;
    padding: 2px 6px;
    font-family: \'Helvetica Neue\', Arial, Helvetica, sans-serif;
    font-size: 10px;
    line-height: 1.5;
    pointer-events: none;
    white-space: nowrap;
">
    Sentinel-2 and Landsat &middot; Summer 2023 &middot; 1,068 tracts
</div>
    '''
if OLD_ATTR in content:
    content = content.replace(OLD_ATTR, '\n    ', 1)

# ─────────────────────────────────────────────────────────────
# 8. Remove emojis throughout
# ─────────────────────────────────────────────────────────────
emoji_map = [
    # Functional button text emojis
    ('&#x1F3D9;&#xFE0F; District View',    'District View'),
    ('&#x2696;&#xFE0F; Compare Tracts',    'Compare Tracts'),
    ('&#x1F331; Simulate Intervention',    'Simulate Intervention'),
    ('&#x1F4CB; Top 20 Priority Zones',    'Top 20 Priority Zones'),
    ('&#x2193; High first',                'High first'),
    ('&#x1F331; Intervention Simulator',   'Intervention Simulator'),
    ('&#x2696;&#xFE0F; Tract Comparison',  'Tract Comparison'),
    ('&#x1F4CB; Share this analysis',      'Share Analysis'),
    # Search icon (now replaced with SVG inline)
    ('&#128269;',                          ''),
    # Export / how to use
    ('&#11015;&#65039; Export Data',       'Export CSV'),
    ('&#9432; How to use',                 'How to Use'),
    # Priority star
    ('&#9733; Higher Priority',            'Higher Priority'),
    # Recommendation type icons
    ("'icon': '&#x1F333;'",               "'icon': '[Tree]'"),
    ("'icon': '&#x1F4A7;'",               "'icon': '[Water]'"),
    ("'icon': '&#x1F331;'",               "'icon': '[Green]'"),
    ("'icon': '&#x1F343;'",               "'icon': '[Leaf]'"),
    # Impact row icons
    ("'&#x1F465;'",                        "'People'"),
    ("'&#x1F333;'",                        "'Trees'"),
    ("'&#x1F4A8;'",                        "'CO2'"),
    ("'&#x1F321;&#xFE0F;'",               "'Temp.'"),
    # Welcome modal icon boxes - replace emoji content with SVG
    ('>&#x1F5FA;&#xFE0F;</div>',          '>&#9718;</div>'),
    ('>&#x1F39A;&#xFE0F;</div>',          '>&#9783;</div>'),
    ('>&#x1F3AF;</div>',                   '>&#9673;</div>'),
    # Clipboard copy buttons
    ("btn.innerHTML = '&#x1F4CB; Share this analysis'", "btn.innerHTML = 'Share Analysis'"),
]

for old, new in emoji_map:
    content = content.replace(old, new)

# ─────────────────────────────────────────────────────────────
# 9. Modify tract bindPopup to include radar chart
# ─────────────────────────────────────────────────────────────
OLD_POPUP = '''\
    geo_json_5923405e0e67b9d1958f351b5ba09684.bindPopup(
    function(layer){
    let div = L.DomUtil.create('div');

    let handleObject = feature => {
        if (feature === null) {
            return \\'\\';
        } else if (typeof(feature)==\\'object\\') {
            return JSON.stringify(feature);
        } else {
            return feature;
        }
    }
    let fields = ["Label", "_ugpi", "_heat", "_green", "_social", "_lst", "_ndvi", "_elderly"];
    let aliases = ["District \\u00b7 Tract", "UGPI Score", "Heat Score", "Green Space Deficit", "Social Vulnerability", "Mean Temperature (\\u00b0C)", "Mean NDVI", "Elderly Population (%)"];
    let table = \\'<table>\\' +
        String(
        fields.map(
        (v,i)=>
        `<tr>
            <th>${aliases[i].toLocaleString()}</th>

            <td>${handleObject(layer.feature.properties[v]).toLocaleString()}</td>
        </tr>`).join(\\'\\'))
    +\\'</table>\\';
    div.innerHTML=table;

    return div
    }
    ,{
  "maxWidth": 360,
  "parseHtml": false,
  "className": "foliumpopup",
});'''

NEW_POPUP = '''\
    var _pendingRadar = null;

    geo_json_5923405e0e67b9d1958f351b5ba09684.bindPopup(
    function(layer){
    let div = L.DomUtil.create(\\'div\\');
    let p = layer.feature.properties;

    let handleObject = feature => {
        if (feature === null) {
            return \\'\\';
        } else if (typeof(feature)==\\'object\\') {
            return JSON.stringify(feature);
        } else {
            return feature;
        }
    }
    let fields = ["Label", "_ugpi", "_heat", "_green", "_social", "_lst", "_ndvi", "_elderly"];
    let aliases = ["District \\u00b7 Tract", "UGPI Score", "Heat Score", "Green Space Deficit", "Social Vulnerability", "Mean Temp. (\\u00b0C)", "Mean NDVI", "Elderly (%)"];
    let table = \\'<table>\\' +
        String(
        fields.map(
        (v,i)=>
        `<tr>
            <th>${aliases[i].toLocaleString()}</th>

            <td>${handleObject(layer.feature.properties[v]).toLocaleString()}</td>
        </tr>`).join(\\'\\'))
    +\\'</table>\\';

    let chartId = \\'rc_\\' + Math.random().toString(36).substr(2,8);
    let chartSection = \\'<div style="padding:10px 14px 14px;border-top:1px solid #edf2f7;">\\'
        + \\'<div style="font-size:9.5px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:8px;">Score Profile</div>\\'
        + \\'<canvas id="\\' + chartId + \\'\\' width="240" height="180"></canvas>\\'
        + \\'</div>\\';

    div.innerHTML = table + chartSection;

    _pendingRadar = {
        id: chartId,
        heat:   parseFloat(p.Heat_Score || 0),
        green:  parseFloat(p.Green_Space_Deficit_Score || 0),
        social: parseFloat(p.Social_Vulnerability_Score || 0)
    };

    return div
    }
    ,{
  "maxWidth": 360,
  "parseHtml": false,
  "className": "foliumpopup",
});

    geo_json_5923405e0e67b9d1958f351b5ba09684.on(\\'popupopen\\', function() {
        if (!_pendingRadar || typeof Chart === \\'undefined\\') return;
        var r = _pendingRadar;
        _pendingRadar = null;
        setTimeout(function() {
            var canvas = document.getElementById(r.id);
            if (!canvas) return;
            new Chart(canvas, {
                type: \\'radar\\',
                data: {
                    labels: [\\'Heat\\', \\'Green Deficit\\', \\'Social Vuln.\\'],
                    datasets: [{
                        data: [r.heat, r.green, r.social],
                        backgroundColor: \\'rgba(253,141,60,0.12)\\',
                        borderColor: \\'#FD8D3C\\',
                        borderWidth: 1.5,
                        pointBackgroundColor: [\\'#FC4E2A\\', \\'#56a85e\\', \\'#7b9fd4\\'],
                        pointBorderColor: \\'#ffffff\\',
                        pointRadius: 4,
                        pointHoverRadius: 5,
                    }]
                },
                options: {
                    responsive: false,
                    scales: {
                        r: {
                            min: 0, max: 10,
                            ticks: { stepSize: 5, font: { size: 9 }, color: \\'#9ca3af\\', backdropColor: \\'transparent\\' },
                            grid: { color: \\'rgba(0,0,0,0.07)\\' },
                            angleLines: { color: \\'rgba(0,0,0,0.07)\\' },
                            pointLabels: { font: { size: 10, weight: \\'600\\' }, color: \\'#374151\\' }
                        }
                    },
                    plugins: { legend: { display: false } },
                    animation: { duration: 280 }
                }
            });
        }, 40);
    });'''

# The file has actual single quotes (not escaped), find and replace
# Let me find the actual popup block using a simpler search
popup_marker = "    geo_json_5923405e0e67b9d1958f351b5ba09684.bindPopup(\n    function(layer){\n    let div = L.DomUtil.create('div');"
popup_end_marker = '  "className": "foliumpopup",\n});\n                     \n    \n            geo_json_5923405e0e67b9d1958f351b5ba09684.addTo('

popup_start = content.find(popup_marker)
popup_end = content.find(popup_end_marker)

assert popup_start != -1, f"Popup start not found"
assert popup_end != -1, f"Popup end not found"

old_popup_block = content[popup_start:popup_end + len(popup_end_marker)]

# Build new popup block
new_popup_block = '''    var _pendingRadar = null;

    geo_json_5923405e0e67b9d1958f351b5ba09684.bindPopup(
    function(layer){
    let div = L.DomUtil.create('div');
    let p = layer.feature.properties;

    let handleObject = feature => {
        if (feature === null) {
            return '';
        } else if (typeof(feature)=='object') {
            return JSON.stringify(feature);
        } else {
            return feature;
        }
    }
    let fields = ["Label", "_ugpi", "_heat", "_green", "_social", "_lst", "_ndvi", "_elderly"];
    let aliases = ["District \\u00b7 Tract", "UGPI Score", "Heat Score", "Green Space Deficit", "Social Vulnerability", "Mean Temp. (\\u00b0C)", "Mean NDVI", "Elderly (%)"];
    let table = '<table>' +
        String(
        fields.map(
        (v,i)=>
        `<tr>
            <th>${aliases[i].toLocaleString()}</th>

            <td>${handleObject(layer.feature.properties[v]).toLocaleString()}</td>
        </tr>`).join(''))
    +'</table>';

    let chartId = 'rc_' + Math.random().toString(36).substr(2,8);
    let chartSection = '<div style="padding:10px 14px 14px;border-top:1px solid #edf2f7;">'
        + '<div style="font-size:9.5px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:8px;">Score Profile</div>'
        + '<canvas id="' + chartId + '" width="240" height="180"></canvas>'
        + '</div>';

    div.innerHTML = table + chartSection;

    _pendingRadar = {
        id: chartId,
        heat:   parseFloat(p.Heat_Score || 0),
        green:  parseFloat(p.Green_Space_Deficit_Score || 0),
        social: parseFloat(p.Social_Vulnerability_Score || 0)
    };

    return div
    }
    ,{
  "maxWidth": 360,
  "parseHtml": false,
  "className": "foliumpopup",
});

    geo_json_5923405e0e67b9d1958f351b5ba09684.on('popupopen', function() {
        if (!_pendingRadar || typeof Chart === 'undefined') return;
        var r = _pendingRadar;
        _pendingRadar = null;
        setTimeout(function() {
            var canvas = document.getElementById(r.id);
            if (!canvas) return;
            new Chart(canvas, {
                type: 'radar',
                data: {
                    labels: ['Heat', 'Green Deficit', 'Social Vuln.'],
                    datasets: [{
                        data: [r.heat, r.green, r.social],
                        backgroundColor: 'rgba(253,141,60,0.12)',
                        borderColor: '#FD8D3C',
                        borderWidth: 1.5,
                        pointBackgroundColor: ['#FC4E2A', '#56a85e', '#7b9fd4'],
                        pointBorderColor: '#ffffff',
                        pointRadius: 4,
                        pointHoverRadius: 5,
                    }]
                },
                options: {
                    responsive: false,
                    scales: {
                        r: {
                            min: 0, max: 10,
                            ticks: { stepSize: 5, font: { size: 9 }, color: '#9ca3af', backdropColor: 'transparent' },
                            grid: { color: 'rgba(0,0,0,0.07)' },
                            angleLines: { color: 'rgba(0,0,0,0.07)' },
                            pointLabels: { font: { size: 10, weight: '600' }, color: '#374151' }
                        }
                    },
                    plugins: { legend: { display: false } },
                    animation: { duration: 280 }
                }
            });
        }, 40);
    });

            geo_json_5923405e0e67b9d1958f351b5ba09684.addTo('''

content = content[:popup_start] + new_popup_block + content[popup_start + len(old_popup_block) + len("            geo_json_5923405e0e67b9d1958f351b5ba09684.addTo("):]

# ─────────────────────────────────────────────────────────────
# 10. Add district ranking JS + call buildDistrictRanking on load
# ─────────────────────────────────────────────────────────────
DISTRICT_RANKING_JS = '''
  window.buildDistrictRanking = function() {
    var el = document.getElementById('district-ranking-list');
    if (!el || !window._districtData) return;
    var districts = _districtData.features.map(function(f) {
      return {
        name: f.properties.District,
        ugpi: parseFloat(f.properties.UGPI),
        rank: parseInt(f.properties._rank) || 99
      };
    }).sort(function(a, b) { return a.rank - b.rank; });

    var html = districts.map(function(d, i) {
      var c = d.ugpi >= 7 ? '#f0a080' : d.ugpi >= 5.5 ? '#fecc5c' : '#80c080';
      var bg = i % 2 === 0 ? 'rgba(255,255,255,0.02)' : 'transparent';
      return '<div style="display:flex;align-items:center;gap:6px;padding:4px 3px;background:' + bg + ';border-radius:3px;">'
        + '<span style="min-width:16px;font-size:9.5px;font-weight:700;color:#2d4055;">' + (i+1) + '</span>'
        + '<span style="flex:1;font-size:10.5px;color:#c8d6e5;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">' + d.name + '</span>'
        + '<span style="font-size:10.5px;font-weight:700;color:' + c + ';min-width:28px;text-align:right;">' + d.ugpi.toFixed(1) + '</span>'
        + '</div>';
    }).join('');
    el.innerHTML = html;
  };
'''

# Insert after the last window.* function before the closing of the main IIFE
# Find a good insertion point: before "window.onload" or just before map init
INSERT_BEFORE = "  window.toggleTop20 = function() {"
assert INSERT_BEFORE in content, "toggleTop20 insertion point not found"
content = content.replace(INSERT_BEFORE, DISTRICT_RANKING_JS + "\n  " + INSERT_BEFORE, 1)

# Call buildDistrictRanking after map ready
# Find where buildTop20 is first called (it's called at the very end of the JS init)
CALL_BUILD = "    buildTop20();\n"
CALL_WITH_DISTRICT = "    buildTop20();\n    buildDistrictRanking();\n"
# Replace only the last occurrence (map init call)
last_idx = content.rfind(CALL_BUILD)
if last_idx != -1:
    content = content[:last_idx] + CALL_WITH_DISTRICT + content[last_idx + len(CALL_BUILD):]

# ─────────────────────────────────────────────────────────────
# 11. Fix welcome modal icon boxes (remove emoji, use styled numbers)
# ─────────────────────────────────────────────────────────────
# Replace the emoji icon boxes with numbered badges
icon_box_style = 'width:38px; height:38px; border-radius:10px; background:rgba(126,184,212,0.12); border:1px solid rgba(126,184,212,0.22); display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:17px;'

for old_char, new_char in [('&#9718;', '1'), ('&#9783;', '2'), ('&#9673;', '3')]:
    content = content.replace(
        f'<div style="{icon_box_style}">{old_char}</div>',
        f'<div style="width:38px;height:38px;border-radius:10px;background:rgba(126,184,212,0.12);border:1px solid rgba(126,184,212,0.22);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:15px;font-weight:700;color:#7eb8d4;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;">{new_char}</div>'
    )

# ─────────────────────────────────────────────────────────────
# 12. Add sidebar scrollbar CSS + misc cleanup
# ─────────────────────────────────────────────────────────────
EXTRA_CSS = '''
<style>
/* Sidebar scrollbar */
#left-sidebar ::-webkit-scrollbar,
#right-sidebar ::-webkit-scrollbar,
#top20-list::-webkit-scrollbar { width: 4px; }
#left-sidebar ::-webkit-scrollbar-track,
#right-sidebar ::-webkit-scrollbar-track,
#top20-list::-webkit-scrollbar-track { background: transparent; }
#left-sidebar ::-webkit-scrollbar-thumb,
#right-sidebar ::-webkit-scrollbar-thumb,
#top20-list::-webkit-scrollbar-thumb { background: rgba(126,184,212,0.25); border-radius: 4px; }

/* Sidebar range input track */
#left-sidebar input[type=range] { -webkit-appearance: none; height: 3px; border-radius: 2px; background: rgba(255,255,255,0.12); outline: none; border: none; }

/* Inter font on all sidebar text */
#left-sidebar *, #right-sidebar * { font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important; }

/* Leaflet layer control - hide the built-in one (we have our own) */
.leaflet-control-layers { display: none !important; }
</style>
'''

# Insert just before </head> or before <body>
body_idx = content.find('\n</head>\n')
if body_idx == -1:
    body_idx = content.find('<body>')
    content = content[:body_idx] + EXTRA_CSS + content[body_idx:]
else:
    content = content[:body_idx] + '\n' + EXTRA_CSS + content[body_idx:]

# ─────────────────────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────────────────────
with open(SRC, "w", encoding="utf-8") as f:
    f.write(content)

print("Done. Map redesigned successfully.")
print(f"Output: {SRC}")
