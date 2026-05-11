"""
Build an interactive Folium HTML map of the Urban Greening Priority Index.
Professional layout for city planners.

Output: outputs/ugpi_interactive_map.html
"""

from pathlib import Path

import geopandas as gpd
import folium
import branca.colormap as cm
import branca.element as bre

DATA_PROC = Path("data/processed")
OUTPUTS   = Path("outputs")

DISTRICT_NAMES = {
    "01": "Ciutat Vella",
    "02": "Eixample",
    "03": "Sants-Montjuïc",
    "04": "Les Corts",
    "05": "Sarrià-Sant Gervasi",
    "06": "Gràcia",
    "07": "Horta-Guinardó",
    "08": "Nou Barris",
    "09": "Sant Andreu",
    "10": "Sant Martí",
}

COLORMAP_COLORS = ["#FFFFB2", "#FECC5C", "#FD8D3C", "#F03B20", "#BD0026"]
VMIN, VMAX = 1.0, 10.0


def load_and_prepare() -> gpd.GeoDataFrame:
    gdf = gpd.read_file(DATA_PROC / "ugpi_final.gpkg")
    gdf["geometry"] = gdf.geometry.simplify(10, preserve_topology=True)
    gdf = gdf.to_crs(4326)

    gdf["District"] = gdf["MUNDISSEC"].str[6:8].map(DISTRICT_NAMES).fillna("Unknown")
    gdf["Label"]    = gdf["District"] + " · T" + gdf["SECCIO"].astype(str).str.zfill(3)

    gdf["_ugpi"]    = gdf["UGPI"].map("{:.2f}".format)
    gdf["_heat"]    = gdf["Heat_Score"].map("{:.2f}".format)
    gdf["_green"]   = gdf["Green_Space_Deficit_Score"].map("{:.2f}".format)
    gdf["_social"]  = gdf["Social_Vulnerability_Score"].map("{:.2f}".format)
    gdf["_lst"]     = gdf["mean_lst"].map("{:.1f}".format)
    gdf["_ndvi"]    = gdf["mean_ndvi"].map("{:.3f}".format)
    gdf["_elderly"] = gdf["pct_elderly"].map("{:.1f}".format)

    print(f"Prepared {len(gdf)} tracts  |  UGPI {gdf['UGPI'].min():.2f}–{gdf['UGPI'].max():.2f}")
    return gdf


INFO_PANEL_HTML = """
<div style="
    position: fixed;
    top: 10px;
    left: 58px;
    z-index: 9999;
    background: #1b2838;
    color: #e8edf3;
    border-radius: 10px;
    padding: 16px 20px 14px;
    width: 292px;
    max-height: calc(100vh - 30px);
    overflow-y: auto;
    box-shadow: 0 6px 28px rgba(0,0,0,0.50);
    font-family: 'Segoe UI', Arial, sans-serif;
    line-height: 1.5;
    pointer-events: none;
">
    <div style="font-size:16px; font-weight:700; letter-spacing:0.01em; color:#ffffff; margin-bottom:4px;">
        Urban Greening Priority Index - Barcelona
    </div>
    <div style="font-size:12px; color:#90b8d0; font-style:italic; margin-bottom:12px;">
        AI-powered decision support for urban planners
    </div>
    <div style="border-top:1px solid rgba(255,255,255,0.12); padding-top:10px;">
        <div style="
            font-size:10px;
            font-weight:700;
            text-transform:uppercase;
            letter-spacing:0.10em;
            color:#7eb8d4;
            margin-bottom:7px;
        ">Methodology - Data Layers</div>
        <div style="font-size:12px; margin-bottom:5px; display:flex; align-items:center; gap:9px;">
            <span style="width:9px;height:9px;border-radius:50%;background:#F03B20;flex-shrink:0;display:inline-block;"></span>
            <span><strong style="color:#f0a080;">Heat</strong> - Land Surface Temperature (LST)</span>
        </div>
        <div style="font-size:12px; margin-bottom:5px; display:flex; align-items:center; gap:9px;">
            <span style="width:9px;height:9px;border-radius:50%;background:#56a85e;flex-shrink:0;display:inline-block;"></span>
            <span><strong style="color:#80c080;">Green Space Deficit</strong> - NDVI coverage gap</span>
        </div>
        <div style="font-size:12px; display:flex; align-items:center; gap:9px;">
            <span style="width:9px;height:9px;border-radius:50%;background:#7b9fd4;flex-shrink:0;display:inline-block;"></span>
            <span><strong style="color:#9ab4e0;">Social Vulnerability</strong> - Elderly population share</span>
        </div>
        <div style="margin-top:9px; font-size:10.5px; color:#6b829e;">
            Equal-weight composite &middot; Summer 2023
        </div>
    </div>
    <div style="border-top:1px solid rgba(255,255,255,0.12); padding-top:10px; margin-top:9px; pointer-events:auto;">
        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.10em; color:#7eb8d4; margin-bottom:7px;">View Layer</div>
        <div style="display:flex; flex-direction:column; gap:5px;">
            <button id="btn-ugpi"   onclick="switchLayer('ugpi')"   style="background:rgba(126,184,212,0.25);color:#e8edf3;border:1px solid #7eb8d4;padding:7px 12px;border-radius:6px;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;font-size:12px;text-align:left;transition:all 0.15s;">UGPI Combined</button>
            <button id="btn-heat"   onclick="switchLayer('heat')"   style="background:rgba(255,255,255,0.07);color:#a0b8cc;border:1px solid rgba(255,255,255,0.12);padding:7px 12px;border-radius:6px;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;font-size:12px;text-align:left;transition:all 0.15s;">Heat</button>
            <button id="btn-green"  onclick="switchLayer('green')"  style="background:rgba(255,255,255,0.07);color:#a0b8cc;border:1px solid rgba(255,255,255,0.12);padding:7px 12px;border-radius:6px;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;font-size:12px;text-align:left;transition:all 0.15s;">Green Space Deficit</button>
            <button id="btn-social" onclick="switchLayer('social')" style="background:rgba(255,255,255,0.07);color:#a0b8cc;border:1px solid rgba(255,255,255,0.12);padding:7px 12px;border-radius:6px;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;font-size:12px;text-align:left;transition:all 0.15s;">Social Vulnerability</button>
        </div>
        <div style="margin-top:4px; padding-top:5px; border-top:1px solid rgba(255,255,255,0.08); display:flex; flex-direction:column; gap:4px;">
            <button id="btn-district" onclick="toggleDistrictView()" style="background:rgba(255,255,255,0.07);color:#a0b8cc;border:1px solid rgba(255,255,255,0.12);padding:7px 12px;border-radius:6px;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;font-size:12px;text-align:left;transition:all 0.15s;width:100%;">&#x1F3D9;&#xFE0F; District View</button>
            <button id="btn-compare" onclick="toggleCompareMode()" style="background:rgba(255,255,255,0.07);color:#a0b8cc;border:1px solid rgba(255,255,255,0.12);padding:7px 12px;border-radius:6px;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;font-size:12px;text-align:left;transition:all 0.15s;width:100%;">&#x2696;&#xFE0F; Compare Tracts</button>
            <button id="btn-sim" onclick="toggleSimMode()" style="background:rgba(255,255,255,0.07);color:#a0b8cc;border:1px solid rgba(255,255,255,0.12);padding:7px 12px;border-radius:6px;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;font-size:12px;text-align:left;transition:all 0.15s;width:100%;">&#x1F331; Simulate Intervention</button>
        </div>
    </div>
    <div id="weight-section" style="border-top:1px solid rgba(255,255,255,0.12); padding-top:10px; margin-top:9px; pointer-events:auto;">
        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.10em; color:#7eb8d4; margin-bottom:7px;">Adjust Weights</div>
        <div style="margin-bottom:7px;">
            <div style="display:flex; justify-content:space-between; font-size:11.5px; margin-bottom:3px;">
                <span style="color:#f0a080; font-weight:600;">Heat</span>
                <span id="val-heat" style="color:#e8edf3;">33%</span>
            </div>
            <input type="range" id="slider-heat" min="0" max="100" value="33" oninput="onWeightSlider('heat')" style="width:100%; accent-color:#f0a080; cursor:pointer; display:block;">
        </div>
        <div style="margin-bottom:7px;">
            <div style="display:flex; justify-content:space-between; font-size:11.5px; margin-bottom:3px;">
                <span style="color:#80c080; font-weight:600;">Green Space</span>
                <span id="val-green" style="color:#e8edf3;">33%</span>
            </div>
            <input type="range" id="slider-green" min="0" max="100" value="33" oninput="onWeightSlider('green')" style="width:100%; accent-color:#56a85e; cursor:pointer; display:block;">
        </div>
        <div style="margin-bottom:7px;">
            <div style="display:flex; justify-content:space-between; font-size:11.5px; margin-bottom:3px;">
                <span style="color:#9ab4e0; font-weight:600;">Social Vulnerability</span>
                <span id="val-social" style="color:#e8edf3;">34%</span>
            </div>
            <input type="range" id="slider-social" min="0" max="100" value="34" oninput="onWeightSlider('social')" style="width:100%; accent-color:#7b9fd4; cursor:pointer; display:block;">
        </div>
        <div id="weight-summary" style="font-size:10.5px; color:#6b829e; text-align:center; margin-bottom:8px;">Heat 33% &middot; Green 33% &middot; Social 34%</div>
        <div style="display:flex; gap:6px;">
            <button onclick="resetWeights()" style="flex:0 0 auto; background:rgba(255,255,255,0.07); color:#a0b8cc; border:1px solid rgba(255,255,255,0.12); padding:8px 12px; border-radius:6px; cursor:pointer; font-family:'Segoe UI',Arial,sans-serif; font-size:12px; font-weight:600; letter-spacing:0.02em; transition:background 0.15s;">Reset</button>
            <button id="btn-recalculate" onclick="recalculateUGPI()" style="flex:1; background:rgba(126,184,212,0.20); color:#e8edf3; border:1px solid #7eb8d4; padding:8px 12px; border-radius:6px; cursor:pointer; font-family:'Segoe UI',Arial,sans-serif; font-size:12px; font-weight:600; letter-spacing:0.02em; transition:background 0.15s;">Recalculate UGPI</button>
        </div>
    </div>
    <div style="border-top:1px solid rgba(255,255,255,0.12); padding-top:10px; margin-top:9px; pointer-events:auto;">
        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.10em; color:#7eb8d4; margin-bottom:7px;">Priority Filter</div>
        <div style="display:flex; justify-content:space-between; font-size:11.5px; margin-bottom:4px;">
            <span style="color:#c8d6e5;">Show tracts with UGPI &ge;</span>
            <span id="filter-val" style="color:#e8edf3; font-weight:600;">1.0</span>
        </div>
        <input type="range" id="slider-filter" min="1" max="10" step="0.1" value="1"
               oninput="onFilterSlider()"
               style="width:100%; accent-color:#7eb8d4; cursor:pointer; display:block; margin-bottom:8px;">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:6px;">
            <span id="filter-counter" style="font-size:10.5px; color:#6b829e;">1068 of 1068 tracts above threshold</span>
            <button onclick="resetFilter()" style="flex:0 0 auto; background:rgba(255,255,255,0.07); color:#a0b8cc; border:1px solid rgba(255,255,255,0.12); padding:4px 10px; border-radius:5px; cursor:pointer; font-family:'Segoe UI',Arial,sans-serif; font-size:11px; font-weight:600; white-space:nowrap; transition:background 0.15s;">Show All</button>
        </div>
    </div>
</div>
"""

LEGEND_HTML = """
<div style="
    position: fixed;
    bottom: 34px;
    right: 10px;
    z-index: 9999;
    background: #1b2838;
    color: #e8edf3;
    border-radius: 10px;
    padding: 14px 18px 12px;
    width: 256px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.45);
    font-family: 'Segoe UI', Arial, sans-serif;
    pointer-events: none;
">
    <div id="legend-label" style="
        font-size:10px;
        font-weight:700;
        text-transform:uppercase;
        letter-spacing:0.10em;
        color:#7eb8d4;
        margin-bottom:9px;
    ">UGPI Score</div>
    <div id="legend-bar" style="
        height:11px;
        border-radius:4px;
        background: linear-gradient(to right, #FFFFB2, #FECC5C, #FD8D3C, #F03B20, #BD0026);
        margin-bottom:6px;
    "></div>
    <div style="display:flex; justify-content:space-between; font-size:11px; color:#a0aec0;">
        <span id="legend-lo">1 - Low priority</span>
        <span id="legend-hi">10 - Highest priority</span>
    </div>
</div>
"""

TOP20_PANEL_HTML = """
<div id="top20-container" style="
    position: fixed;
    top: 120px;
    right: 10px;
    z-index: 9999;
    width: 256px;
    font-family: 'Segoe UI', Arial, sans-serif;
">
    <button onclick="toggleTop20()" style="
        display: block;
        width: 100%;
        background: #1b2838;
        color: #e8edf3;
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 8px;
        padding: 8px 14px;
        cursor: pointer;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.02em;
        box-shadow: 0 4px 14px rgba(0,0,0,0.45);
        text-align: left;
    ">&#x1F4CB; Top 20 Priority Zones</button>
    <div id="top20-panel" style="
        display: none;
        background: #1b2838;
        color: #e8edf3;
        border-radius: 10px;
        padding: 14px 14px 10px;
        max-height: calc(100vh - 240px);
        overflow-y: auto;
        box-shadow: 0 6px 28px rgba(0,0,0,0.50);
        margin-top: 6px;
    ">
        <div style="display:flex; align-items:center; justify-content:space-between; padding-bottom:7px; border-bottom:1px solid rgba(255,255,255,0.12); margin-bottom:4px;">
            <span id="top20-header-label" style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.10em; color:#7eb8d4;">Top 20 &middot; UGPI</span>
            <button id="top20-sort-btn" onclick="toggleTop20Sort()" style="font-size:10px; font-weight:600; color:#7eb8d4; background:transparent; border:1px solid rgba(126,184,212,0.30); border-radius:4px; padding:2px 7px; cursor:pointer; font-family:'Segoe UI',Arial,sans-serif; white-space:nowrap; transition:all 0.15s;">&#x2193; High first</button>
        </div>
        <div style="display:flex; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#4a6580; padding:5px 4px 5px; border-bottom:1px solid rgba(255,255,255,0.08); margin-bottom:2px;">
            <span style="min-width:22px;">#</span>
            <span style="flex:1; padding-left:2px;">District</span>
            <span>Score</span>
        </div>
        <div id="top20-list"></div>
    </div>
</div>
"""

POPUP_CSS = """
<style>
.leaflet-popup-content-wrapper {
    border-radius: 10px;
    padding: 0;
    box-shadow: 0 8px 28px rgba(0,0,0,0.22);
    font-family: 'Segoe UI', Arial, sans-serif;
    overflow: hidden;
}
.leaflet-popup-content {
    margin: 0;
    min-width: 280px;
}
.leaflet-popup-content table {
    border-collapse: collapse;
    width: 100%;
    margin: 0;
}
.leaflet-popup-content table tr td {
    padding: 6px 14px;
    font-size: 12.5px;
    color: #2d3748;
    border-bottom: 1px solid #f0f4f8;
    vertical-align: middle;
}
.leaflet-popup-content table tr td:first-child {
    color: #4a5568;
    font-weight: 600;
    white-space: nowrap;
    padding-right: 16px;
    background: #f7fafc;
    width: 44%;
}
.leaflet-popup-content table tr:first-child td {
    font-weight: 700;
    font-size: 13.5px;
    color: #1a202c;
    padding-top: 14px;
    padding-bottom: 12px;
    border-bottom: 2px solid #ebf0f6;
    background: #ffffff;
}
.leaflet-popup-content table tr:first-child td:first-child {
    background: #ffffff;
}
.leaflet-popup-content table tr:last-child td {
    border-bottom: none;
    padding-bottom: 12px;
}
.leaflet-popup-tip-container {
    margin-top: -1px;
}
.district-tip {
    background: rgba(27,40,56,0.93) !important;
    color: #e8edf3 !important;
    border: none !important;
    border-radius: 7px !important;
    padding: 8px 13px !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.35) !important;
    font-family: 'Segoe UI', Arial, sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
.district-tip::before {
    display: none !important;
}
</style>
"""

LAYER_TOGGLE_JS_TEMPLATE = """
<script>
(function() {{
  var _scales = {{
    ugpi:   {{ colors: ["#FFFFB2","#FECC5C","#FD8D3C","#F03B20","#BD0026"],         vmin:1, vmax:10 }},
    heat:   {{ colors: ["#FFFFCC","#FFEDA0","#FED976","#FEB24C","#FC4E2A","#E31A1C","#BD0026"], vmin:1, vmax:10 }},
    green:  {{ colors: ["#FFFFB2","#FECC5C","#FD8D3C","#F03B20","#BD0026"],         vmin:1, vmax:10 }},
    social: {{ colors: ["#FFF7FB","#D0D1E6","#74A9CF","#0570B0","#023858"],         vmin:1, vmax:10 }}
  }};
  var _fields = {{
    ugpi: "UGPI", heat: "Heat_Score",
    green: "Green_Space_Deficit_Score", social: "Social_Vulnerability_Score"
  }};
  var _layerNames = {{
    ugpi: "UGPI", heat: "Heat", green: "Green Space Deficit", social: "Social Vulnerability"
  }};
  var _legendCfg = {{
    ugpi:   {{ label: "UGPI Score",                 gradient: "linear-gradient(to right,#FFFFB2,#FECC5C,#FD8D3C,#F03B20,#BD0026)",                 lo: "1 - Low priority",      hi: "10 - Highest priority" }},
    heat:   {{ label: "Heat Score",                 gradient: "linear-gradient(to right,#FFFFCC,#FFEDA0,#FED976,#FEB24C,#FC4E2A,#E31A1C,#BD0026)", lo: "1 - Cool",              hi: "10 - Extreme heat" }},
    green:  {{ label: "Green Space Deficit Score",  gradient: "linear-gradient(to right,#FFFFB2,#FECC5C,#FD8D3C,#F03B20,#BD0026)",                 lo: "1 - Low deficit",       hi: "10 - High deficit" }},
    social: {{ label: "Social Vulnerability Score", gradient: "linear-gradient(to right,#FFF7FB,#D0D1E6,#74A9CF,#0570B0,#023858)",                 lo: "1 - Low vulnerability", hi: "10 - High vulnerability" }}
  }};

  function _hex2rgb(h) {{
    return [parseInt(h.slice(1,3),16), parseInt(h.slice(3,5),16), parseInt(h.slice(5,7),16)];
  }}
  function _rgb2hex(r,g,b) {{
    return '#'+[r,g,b].map(function(x){{var s=Math.round(x).toString(16);return s.length<2?'0'+s:s;}}).join('');
  }}
  function _color(val, scale) {{
    var t = Math.max(0, Math.min(1, (val - scale.vmin) / (scale.vmax - scale.vmin)));
    var n = scale.colors.length - 1;
    var i = Math.min(Math.floor(t * n), n - 1);
    var f = t * n - i;
    var c0 = _hex2rgb(scale.colors[i]), c1 = _hex2rgb(scale.colors[i + 1]);
    return _rgb2hex(c0[0]+f*(c1[0]-c0[0]), c0[1]+f*(c1[1]-c0[1]), c0[2]+f*(c1[2]-c0[2]));
  }}

  function _ordinal(n) {{
    var s = ['th','st','nd','rd'], v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
  }}

  function _setLayerBtnState(activeKey) {{
    ['ugpi','heat','green','social'].forEach(function(k) {{
      var btn = document.getElementById('btn-' + k);
      if (!btn) return;
      var on = (k === activeKey);
      btn.style.background  = on ? 'rgba(126,184,212,0.25)' : 'rgba(255,255,255,0.07)';
      btn.style.color       = on ? '#e8edf3'                : '#a0b8cc';
      btn.style.borderColor = on ? '#7eb8d4'                : 'rgba(255,255,255,0.12)';
    }});
  }}

  function _setDistrictBtnState(active) {{
    var btn = document.getElementById('btn-district');
    if (!btn) return;
    btn.style.background  = active ? 'rgba(126,184,212,0.25)' : 'rgba(255,255,255,0.07)';
    btn.style.color       = active ? '#e8edf3'                : '#a0b8cc';
    btn.style.borderColor = active ? '#7eb8d4'                : 'rgba(255,255,255,0.12)';
  }}

  function _setWeightControlsEnabled(enabled) {{
    var section = document.getElementById('weight-section');
    if (!section) return;
    section.style.opacity       = enabled ? '1'    : '0.4';
    section.style.pointerEvents = enabled ? 'auto' : 'none';
  }}

  function _updateLegend(key) {{
    var cfg = _legendCfg[key];
    if (!cfg) return;
    var lbl = document.getElementById('legend-label');
    var bar = document.getElementById('legend-bar');
    var lo  = document.getElementById('legend-lo');
    var hi  = document.getElementById('legend-hi');
    if (lbl) lbl.textContent      = cfg.label;
    if (bar) bar.style.background = cfg.gradient;
    if (lo)  lo.textContent       = cfg.lo;
    if (hi)  hi.textContent       = cfg.hi;
  }}

  var _activeKey      = 'ugpi';
  var _top20Ascending = false;
  var _districtLayer  = null;
  var _inDistrictView = false;
  var _map            = null;
  var _searchHighlight     = null;
  var _searchDebounceTimer = null;
  var _searchSuggestions   = [];
  var _filterThreshold     = 1.0;
  var _compareMode         = false;
  var _compareTracts       = [];
  var _simMode             = false;
  var _simLyr              = null;
  var _simOrigProps        = null;
  var _simCurrentRec       = '';

  function _getMap() {{
    if (!_map) _map = window.{layer_var}._map;
    return _map;
  }}

  function _hideDropdown() {{
    var dd = document.getElementById('search-dropdown');
    if (dd) dd.style.display = 'none';
  }}

  function _showDropdown(results) {{
    var dd = document.getElementById('search-dropdown');
    if (!dd) return;
    dd.innerHTML = '';
    if (!results || !results.length) {{ dd.style.display = 'none'; return; }}
    results.forEach(function(item) {{
      var li = document.createElement('li');
      li.textContent = item.display_name;
      li.style.cssText = 'padding:9px 14px;font-size:12px;color:#c8d6e5;cursor:pointer;line-height:1.4;border-bottom:1px solid rgba(255,255,255,0.06);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;transition:background 0.12s;';
      li.addEventListener('mouseover', function() {{ this.style.background = 'rgba(126,184,212,0.15)'; }});
      li.addEventListener('mouseout',  function() {{ this.style.background = 'transparent'; }});
      li.addEventListener('mousedown', function(e) {{
        e.preventDefault();
        var inp = document.getElementById('search-input');
        if (inp) inp.value = item.display_name;
        var clrBtn = document.getElementById('search-clear');
        if (clrBtn) clrBtn.style.display = 'flex';
        _hideDropdown();
        _flyAndHighlight(parseFloat(item.lat), parseFloat(item.lon));
      }});
      dd.appendChild(li);
    }});
    dd.style.display = 'block';
  }}

  function _flyAndHighlight(lat, lng) {{
    _getMap().flyTo([lat, lng], 15, {{ duration: 1.2 }});
    _clearSearchHighlight();
    var found = null;
    window.{layer_var}.eachLayer(function(lyr) {{
      if (found) return;
      var geom = lyr.feature && lyr.feature.geometry;
      if (!geom) return;
      var rings = geom.type === 'Polygon'
        ? [geom.coordinates[0]]
        : geom.type === 'MultiPolygon'
          ? geom.coordinates.map(function(poly) {{ return poly[0]; }})
          : [];
      if (rings.some(function(ring) {{ return _pointInRing(lat, lng, ring); }})) {{
        found = lyr;
      }}
    }});
    if (found) {{
      _searchHighlight = found;
      found.setStyle({{ color: '#ffffff', weight: 3.5, opacity: 1 }});
      var pulseCount = 0, bright = true;
      var iv = setInterval(function() {{
        bright = !bright;
        found.setStyle({{ weight: bright ? 3.5 : 1.2, opacity: bright ? 1 : 0.15 }});
        if (++pulseCount >= 6) clearInterval(iv);
      }}, 300);
      setTimeout(function() {{ found.openPopup(); }}, 1350);
    }}
  }}

  function _pointInRing(lat, lng, ring) {{
    var inside = false;
    for (var i = 0, j = ring.length - 1; i < ring.length; j = i++) {{
      var rLng = ring[i][0], rLat = ring[i][1];
      var pLng = ring[j][0], pLat = ring[j][1];
      if (((rLat > lat) !== (pLat > lat)) &&
          (lng < (pLng - rLng) * (lat - rLat) / (pLat - rLat) + rLng)) {{
        inside = !inside;
      }}
    }}
    return inside;
  }}

  function _clearSearchHighlight() {{
    if (!_searchHighlight) return;
    var p = _searchHighlight.feature && _searchHighlight.feature.properties;
    if (p) {{
      var val = parseFloat(p[_fields[_activeKey]]);
      var dim = parseFloat(p.UGPI) < _filterThreshold;
      _searchHighlight.setStyle({{
        color: 'white', weight: 0.4,
        opacity: dim ? 0.15 : 1,
        fillColor: _color(val, _scales[_activeKey]),
        fillOpacity: dim ? 0.08 : 0.80
      }});
    }}
    _searchHighlight = null;
  }}

  function _setCompareBtnState(active) {{
    var btn = document.getElementById('btn-compare');
    if (!btn) return;
    btn.style.background  = active ? 'rgba(254,204,92,0.20)' : 'rgba(255,255,255,0.07)';
    btn.style.color       = active ? '#fecc5c'               : '#a0b8cc';
    btn.style.borderColor = active ? '#fecc5c'               : 'rgba(255,255,255,0.12)';
  }}

  function _restoreCompareStyle(lyr) {{
    var p = lyr.feature && lyr.feature.properties;
    if (!p) return;
    var el = lyr.getElement && lyr.getElement();
    if (el) el.style.filter = '';
    var val = parseFloat(p[_fields[_activeKey]]);
    var dim = parseFloat(p.UGPI) < _filterThreshold;
    lyr.setStyle({{
      color: 'white', weight: 0.4,
      opacity: dim ? 0.15 : 1,
      fillColor: _color(val, _scales[_activeKey]),
      fillOpacity: dim ? 0.08 : 0.80
    }});
  }}

  function _hideComparePanel() {{
    var panel = document.getElementById('compare-panel');
    if (panel) panel.style.display = 'none';
  }}

  function _barRows(metrics, side) {{
    var html = '';
    metrics.forEach(function(m) {{
      var val = side === 0 ? m.val0 : m.val1;
      var pct = Math.max(0, Math.min(100, val / 10 * 100));
      html += '<div style="margin-bottom:8px;">';
      html += '<div style="display:flex;justify-content:space-between;font-size:10.5px;color:#8a9bb0;margin-bottom:3px;">';
      html += '<span>' + m.label + '</span><span style="color:#e8edf3;font-weight:600;">' + val.toFixed(2) + '</span>';
      html += '</div>';
      html += '<div style="background:rgba(255,255,255,0.08);border-radius:3px;height:8px;overflow:hidden;">';
      html += '<div style="width:' + pct + '%;height:100%;background:' + m.color + ';border-radius:3px;"></div>';
      html += '</div></div>';
    }});
    return html;
  }}

  function _buildComparePanel() {{
    var p0 = _compareTracts[0].feature.properties;
    var p1 = _compareTracts[1].feature.properties;
    var u0 = parseFloat(p0.UGPI), u1 = parseFloat(p1.UGPI);
    var metrics = [
      {{ label: 'UGPI',          color: '#FD8D3C', val0: u0,                                             val1: u1 }},
      {{ label: 'Heat',          color: '#FC4E2A', val0: parseFloat(p0.Heat_Score),                      val1: parseFloat(p1.Heat_Score) }},
      {{ label: 'Green Deficit', color: '#56a85e', val0: parseFloat(p0.Green_Space_Deficit_Score),       val1: parseFloat(p1.Green_Space_Deficit_Score) }},
      {{ label: 'Social Vuln',   color: '#7b9fd4', val0: parseFloat(p0.Social_Vulnerability_Score),     val1: parseFloat(p1.Social_Vulnerability_Score) }}
    ];
    var diff = u0 - u1;
    var winTag = function(side) {{
      if (Math.abs(diff) < 0.005) return '<div style="font-size:10px;color:#6b829e;margin-bottom:10px;">Equal Priority</div>';
      var wins = (side === 0 && diff > 0) || (side === 1 && diff < 0);
      return wins
        ? '<div style="font-size:10px;font-weight:700;color:#fecc5c;margin-bottom:10px;">&#9733; Higher Priority</div>'
        : '<div style="font-size:10px;color:#6b829e;margin-bottom:10px;">Lower Priority</div>';
    }};
    var col = '<div style="flex:1;min-width:0;">';
    var lbl0 = '<div style="font-size:12px;font-weight:700;color:#e8edf3;margin-bottom:4px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">' + (p0.Label || 'Tract A') + '</div>';
    var lbl1 = '<div style="font-size:12px;font-weight:700;color:#e8edf3;margin-bottom:4px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">' + (p1.Label || 'Tract B') + '</div>';
    var div = '<div style="width:1px;background:rgba(255,255,255,0.10);flex-shrink:0;"></div>';
    var html =
      '<div style="display:flex;gap:20px;">' +
        col + lbl0 + winTag(0) + _barRows(metrics, 0) + '</div>' +
        div +
        col + lbl1 + winTag(1) + _barRows(metrics, 1) + '</div>' +
      '</div>';
    var content = document.getElementById('compare-content');
    if (content) content.innerHTML = html;
    var panel = document.getElementById('compare-panel');
    if (panel) panel.style.display = 'block';
  }}

  function _handleCompareClick(lyr) {{
    var idx = -1;
    _compareTracts.forEach(function(t, i) {{ if (t === lyr) idx = i; }});
    if (idx !== -1) {{
      _restoreCompareStyle(_compareTracts[idx]);
      _compareTracts.splice(idx, 1);
      _hideComparePanel();
      return;
    }}
    if (_compareTracts.length >= 2) {{
      _restoreCompareStyle(_compareTracts[0]);
      _compareTracts.shift();
    }}
    var el = lyr.getElement && lyr.getElement();
    if (el) el.style.filter = 'drop-shadow(0 0 5px rgba(255,255,255,0.85))';
    lyr.setStyle({{ color: '#ffffff', weight: 3.5, opacity: 1, fillOpacity: 0.90 }});
    _compareTracts.push(lyr);
    if (_compareTracts.length === 2) {{
      _buildComparePanel();
    }} else {{
      _hideComparePanel();
    }}
  }}

  function _setSimBtnState(active) {{
    var btn = document.getElementById('btn-sim');
    if (!btn) return;
    btn.style.background  = active ? 'rgba(86,168,94,0.20)'  : 'rgba(255,255,255,0.07)';
    btn.style.color       = active ? '#80c080'               : '#a0b8cc';
    btn.style.borderColor = active ? '#56a85e'               : 'rgba(255,255,255,0.12)';
  }}

  function _ndviToGreen(ndvi) {{
    var score = 1 + 9 * (_SIM_NDVI_MAX - ndvi) / (_SIM_NDVI_MAX - _SIM_NDVI_MIN);
    return Math.max(1, Math.min(10, score));
  }}

  function _lstToHeat(lst) {{
    var score = 1 + 9 * (lst - _SIM_LST_MIN) / (_SIM_LST_MAX - _SIM_LST_MIN);
    return Math.max(1, Math.min(10, score));
  }}

  function _getRecommendation(green, heat, social) {{
    if (green > 7 && heat > 7 && social > 7) return {{ type: 'Urban Forest / Priority Zone', icon: '&#x1F333;', detail: 'All three stressors are critical. Large-scale tree planting and shaded public spaces recommended.' }};
    if (heat > 7 && green > 6) return {{ type: 'Green Cooling Corridor', icon: '&#x1F4A7;', detail: 'High heat with low greenery. Prioritise street trees, green roofs, and permeable surfaces.' }};
    if (social > 7) return {{ type: 'Community Garden', icon: '&#x1F331;', detail: 'Socially vulnerable population. Participatory green spaces improve wellbeing and heat resilience.' }};
    if (green > 7) return {{ type: 'Street Tree Planting', icon: '&#x1F333;', detail: 'Green space deficit is dominant. Street-level tree planting can quickly raise NDVI.' }};
    return {{ type: 'Incremental Greening', icon: '&#x1F343;', detail: 'Moderate pressure across indicators. Small-scale pocket parks and wall greening advised.' }};
  }}

  function _impactRow(icon, label, value) {{
    return '<div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:7px;">' +
      '<span style="font-size:16px;flex-shrink:0;line-height:1.4;">' + icon + '</span>' +
      '<div>' +
        '<div style="font-size:10px;color:#6b829e;text-transform:uppercase;letter-spacing:0.07em;">' + label + '</div>' +
        '<div style="font-size:12px;font-weight:600;color:#e8edf3;">' + value + '</div>' +
      '</div>' +
    '</div>';
  }}

  function _restoreSimStyle() {{
    if (!_simLyr) return;
    var el = _simLyr.getElement && _simLyr.getElement();
    if (el) el.style.filter = '';
    var p = _simLyr.feature && _simLyr.feature.properties;
    if (p) {{
      var val = parseFloat(p[_fields[_activeKey]]);
      var dim = parseFloat(p.UGPI) < _filterThreshold;
      _simLyr.setStyle({{
        color: 'white', weight: 0.4, opacity: dim ? 0.15 : 1,
        fillColor: _color(val, _scales[_activeKey]),
        fillOpacity: dim ? 0.08 : 0.80
      }});
    }}
    _simLyr = null;
    _simOrigProps = null;
  }}

  function _hideSimPanel() {{
    var panel = document.getElementById('sim-panel');
    if (panel) panel.style.display = 'none';
  }}

  function _showSimInstruction() {{
    var instrEl = document.getElementById('sim-instruction');
    if (instrEl) instrEl.style.display = 'block';
    var labelEl = document.getElementById('sim-tract-label');
    if (labelEl) labelEl.style.display = 'none';
    var slidersEl = document.getElementById('sim-sliders');
    if (slidersEl) slidersEl.style.display = 'none';
    var panel = document.getElementById('sim-panel');
    if (panel) panel.style.display = 'block';
  }}

  function _updateSimPanel() {{
    if (!_simLyr || !_simOrigProps) return;
    var dNDVI = parseFloat(document.getElementById('sim-ndvi').value);
    var dLST  = parseFloat(document.getElementById('sim-lst').value);
    document.getElementById('sim-ndvi-val').textContent = dNDVI.toFixed(2);
    document.getElementById('sim-lst-val').textContent  = dLST.toFixed(1);
    var newNDVI  = Math.min(1.0, _simOrigProps.ndvi + dNDVI);
    var newLST   = _simOrigProps.lst - dLST;
    var newGreen = _ndviToGreen(newNDVI);
    var newHeat  = _lstToHeat(newLST);
    var hw = parseInt(document.getElementById('slider-heat').value)  / 100;
    var gw = parseInt(document.getElementById('slider-green').value) / 100;
    var sw = parseInt(document.getElementById('slider-social').value)/ 100;
    var beforeUGPI = hw * _simOrigProps.heat  + gw * _simOrigProps.green + sw * _simOrigProps.social;
    var newUGPI    = hw * newHeat             + gw * newGreen            + sw * _simOrigProps.social;
    var rows = [
      {{ label: 'UGPI Score',    orig: beforeUGPI,          next: newUGPI   }},
      {{ label: 'Heat Score',    orig: _simOrigProps.heat,  next: newHeat   }},
      {{ label: 'Green Deficit', orig: _simOrigProps.green, next: newGreen  }}
    ];
    var html = '<div style="background:rgba(255,255,255,0.04);border-radius:8px;padding:10px 12px;margin-bottom:8px;">';
    rows.forEach(function(r) {{
      var delta    = r.next - r.orig;
      var improved = delta < -0.005;
      var noChange = Math.abs(delta) <= 0.005;
      var nextCol  = improved ? '#80c080' : '#e8edf3';
      var dTag     = noChange ? '' :
        '<span style="font-size:10px;font-weight:600;color:' + (improved ? '#56a85e' : '#e05050') + ';min-width:36px;text-align:right;">' +
        (delta >= 0 ? '+' : '') + delta.toFixed(2) + '</span>';
      html +=
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">' +
          '<span style="font-size:10.5px;color:#8a9bb0;">' + r.label + '</span>' +
          '<div style="display:flex;align-items:center;gap:5px;">' +
            '<span style="color:#a0b8cc;font-size:11px;">' + r.orig.toFixed(2) + '</span>' +
            '<span style="color:#3a5068;font-size:10px;">&#8594;</span>' +
            '<span style="color:' + nextCol + ';font-weight:600;font-size:11px;">' + r.next.toFixed(2) + '</span>' +
            dTag +
          '</div>' +
        '</div>';
    }});
    html += '</div>';
    document.getElementById('sim-scores').innerHTML = html;
    var trees = Math.round(dNDVI * _simAvgArea / 50);
    var treesEl = document.getElementById('sim-trees');
    if (treesEl) {{
      treesEl.textContent = dNDVI > 0.005
        ? '≈ ' + trees.toLocaleString() + ' trees planted (1 tree / 50 m²)'
        : '';
    }}

    // Recommended intervention
    var rec = _getRecommendation(newGreen, newHeat, _simOrigProps.social);
    _simCurrentRec = rec.type;
    var recEl = document.getElementById('sim-recommendation');
    if (recEl) {{
      recEl.innerHTML =
        '<div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:10px;margin-top:6px;margin-bottom:10px;">' +
          '<div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.10em;color:#7eb8d4;margin-bottom:8px;">Recommended Intervention</div>' +
          '<div style="display:flex;align-items:flex-start;gap:9px;background:rgba(126,184,212,0.08);border-radius:8px;padding:10px 12px;">' +
            '<span style="font-size:22px;flex-shrink:0;">' + rec.icon + '</span>' +
            '<div>' +
              '<div style="font-size:12px;font-weight:700;color:#e8edf3;margin-bottom:4px;">' + rec.type + '</div>' +
              '<div style="font-size:11px;color:#6b829e;line-height:1.5;">' + rec.detail + '</div>' +
            '</div>' +
          '</div>' +
        '</div>';
    }}

    // Estimated impact
    var pop        = _simOrigProps.pop || 0;
    var co2PerYear = trees * 22;
    var tempReduc  = Math.round(dNDVI / 0.05 * 0.5 * 10) / 10;
    var impactEl   = document.getElementById('sim-impact');
    if (impactEl) {{
      var impHtml =
        '<div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:10px;margin-bottom:10px;">' +
          '<div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.10em;color:#7eb8d4;margin-bottom:10px;">Estimated Impact</div>';
      impHtml += _impactRow('&#x1F465;', 'People Benefited',        pop > 0 ? pop.toLocaleString() + ' residents' : 'N/A');
      impHtml += _impactRow('&#x1F333;', 'Trees Required',          dNDVI > 0.005 ? '≈ ' + trees.toLocaleString() + ' trees' : 'No planting modelled');
      impHtml += _impactRow('&#x1F4A8;', 'CO₂ Absorbed / yr',  co2PerYear > 0 ? '≈ ' + co2PerYear.toLocaleString() + ' kg CO₂' : 'No change');
      impHtml += _impactRow('&#x1F321;&#xFE0F;', 'Est. Temp. Reduction', tempReduc > 0 ? '−' + tempReduc.toFixed(1) + ' °C' : 'No change');
      impHtml += '</div>';
      impactEl.innerHTML = impHtml;
    }}

    // Share button — injected once, stays for subsequent slider updates
    var shareEl = document.getElementById('sim-share');
    if (shareEl && !shareEl.hasChildNodes()) {{
      shareEl.innerHTML =
        '<div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:10px;">' +
          '<button id="sim-share-btn" onclick="shareSimAnalysis()" style="width:100%;background:rgba(126,184,212,0.12);color:#7eb8d4;border:1px solid rgba(126,184,212,0.35);border-radius:7px;padding:9px 14px;cursor:pointer;font-size:12px;font-weight:600;transition:all 0.15s;" onmouseover="this.style.background=\\'rgba(126,184,212,0.22)\\'" onmouseout="this.style.background=\\'rgba(126,184,212,0.12)\\'">&#x1F4CB; Share this analysis</button>' +
        '</div>';
    }}

    _simLyr.setStyle({{ fillColor: _color(newUGPI, _scales.ugpi) }});
  }}

  function _buildSimPanel(lyr) {{
    _simLyr = lyr;
    var p = lyr.feature.properties;
    _simOrigProps = {{
      ndvi:   parseFloat(p._ndvi),
      lst:    parseFloat(p._lst),
      green:  parseFloat(p.Green_Space_Deficit_Score),
      heat:   parseFloat(p.Heat_Score),
      social: parseFloat(p.Social_Vulnerability_Score),
      pop:    parseInt(p.total_pop) || 0
    }};
    var el = lyr.getElement && lyr.getElement();
    if (el) el.style.filter = 'drop-shadow(0 0 5px rgba(86,168,94,0.90))';
    lyr.setStyle({{ color: '#80c080', weight: 3.5, opacity: 1, fillOpacity: 0.90 }});
    var ndviSl = document.getElementById('sim-ndvi');
    var lstSl  = document.getElementById('sim-lst');
    if (ndviSl) ndviSl.value = 0;
    if (lstSl)  lstSl.value  = 0;
    var instrEl = document.getElementById('sim-instruction');
    if (instrEl) instrEl.style.display = 'none';
    var labelEl = document.getElementById('sim-tract-label');
    if (labelEl) {{ labelEl.textContent = p.Label || 'Unknown'; labelEl.style.display = 'block'; }}
    var slidersEl = document.getElementById('sim-sliders');
    if (slidersEl) slidersEl.style.display = 'block';
    var shareEl = document.getElementById('sim-share');
    if (shareEl) shareEl.innerHTML = '';
    var panel = document.getElementById('sim-panel');
    if (panel) panel.style.display = 'block';
    _updateSimPanel();
  }}

  function _applyFilter() {{
    var thresh = _filterThreshold;
    var above = 0, total = 0;
    window.{layer_var}.eachLayer(function(lyr) {{
      var p = lyr.feature && lyr.feature.properties;
      if (!p) return;
      total++;
      var ugpi = parseFloat(p.UGPI);
      if (ugpi >= thresh) {{
        above++;
        lyr.setStyle({{ fillOpacity: 0.80, opacity: 1 }});
      }} else {{
        lyr.setStyle({{ fillOpacity: 0.08, opacity: 0.15 }});
      }}
    }});
    var counterEl = document.getElementById('filter-counter');
    if (counterEl) counterEl.textContent = above + ' of ' + total + ' tracts above threshold';
  }}

  function _replaceHoverHandlers() {{
    window.{layer_var}.eachLayer(function(lyr) {{
      lyr.off('mouseover').off('mouseout');
      lyr.on('mouseover', function(e) {{
        if (e.target !== e.propagatedFrom) return;
        var p = e.target.feature && e.target.feature.properties;
        if (!p) return;
        var v = parseFloat(p[_fields[_activeKey]]);
        e.target.setStyle({{ fillColor: _color(v, _scales[_activeKey]), color: '#e2e8f0', weight: 2.2, fillOpacity: 0.95 }});
      }});
      lyr.on('mouseout', function(e) {{
        if (e.target !== e.propagatedFrom) return;
        var p = e.target.feature && e.target.feature.properties;
        if (!p) return;
        var isSelected = _compareTracts.indexOf(e.target) !== -1;
        if (isSelected) return;
        var v = parseFloat(p[_fields[_activeKey]]);
        var dim = parseFloat(p.UGPI) < _filterThreshold;
        e.target.setStyle({{ fillColor: _color(v, _scales[_activeKey]), color: 'white', weight: 0.4, fillOpacity: dim ? 0.08 : 0.80, opacity: dim ? 0.15 : 1 }});
      }});
      lyr.on('click', function(e) {{
        if (_compareMode) {{
          L.DomEvent.stopPropagation(e);
          _handleCompareClick(e.target);
          setTimeout(function() {{ _getMap().closePopup(); }}, 10);
          return;
        }}
        if (_simMode) {{
          L.DomEvent.stopPropagation(e);
          if (_simLyr && _simLyr !== e.target) _restoreSimStyle();
          _buildSimPanel(e.target);
          setTimeout(function() {{ _getMap().closePopup(); }}, 10);
        }}
      }});
    }});
  }}

  function _makeDistrictLayer() {{
    return L.geoJSON(_districtData, {{
      style: function(feat) {{
        return {{
          fillColor: _color(feat.properties.UGPI, _scales.ugpi),
          color: 'white',
          weight: 1.5,
          fillOpacity: 0.82
        }};
      }},
      onEachFeature: function(feat, lyr) {{
        var p = feat.properties;
        var rank = _ordinal(p._rank);
        lyr.bindTooltip(
          '<strong>' + p.District + '</strong> · UGPI ' + parseFloat(p.UGPI).toFixed(2),
          {{ sticky: true, opacity: 1, className: 'district-tip' }}
        );
        lyr.bindPopup(
          '<table>' +
          '<tr><td>District</td><td>' + p.District + '</td></tr>' +
          '<tr><td>Ranking</td><td>' + rank + ' most critical</td></tr>' +
          '<tr><td>UGPI Score</td><td>' + parseFloat(p.UGPI).toFixed(2) + '</td></tr>' +
          '<tr><td>Heat Score</td><td>' + parseFloat(p.Heat_Score).toFixed(2) + '</td></tr>' +
          '<tr><td>Green Space Deficit</td><td>' + parseFloat(p.Green_Space_Deficit_Score).toFixed(2) + '</td></tr>' +
          '<tr><td>Social Vulnerability</td><td>' + parseFloat(p.Social_Vulnerability_Score).toFixed(2) + '</td></tr>' +
          '</table>',
          {{ maxWidth: 320 }}
        );
        lyr.on('mouseover', function() {{
          lyr.setStyle({{ weight: 2.5, color: '#e2e8f0' }});
        }});
        lyr.on('mouseout', function() {{
          _districtLayer.resetStyle(lyr);
        }});
      }}
    }});
  }}

  window.toggleDistrictView = function() {{
    var map = _getMap();
    if (!map) return;
    if (_inDistrictView) {{
      if (_districtLayer) map.removeLayer(_districtLayer);
      window.{layer_var}.addTo(map);
      _inDistrictView = false;
      _setDistrictBtnState(false);
      _setLayerBtnState(_activeKey);
      _setWeightControlsEnabled(_activeKey === 'ugpi');
      _updateLegend(_activeKey);
    }} else {{
      map.removeLayer(window.{layer_var});
      if (!_districtLayer) _districtLayer = _makeDistrictLayer();
      _districtLayer.addTo(map);
      _inDistrictView = true;
      _setDistrictBtnState(true);
      _setLayerBtnState(null);
    }}
  }};

  var _top20Layers = [];

  window.buildTop20 = function() {{
    var field = _fields[_activeKey];
    var rows = [];
    window.{layer_var}.eachLayer(function(lyr) {{
      var p = lyr.feature && lyr.feature.properties;
      if (!p) return;
      if (parseFloat(p.UGPI) < _filterThreshold) return;
      rows.push({{ lyr: lyr, score: parseFloat(p[field]), label: p.Label || 'Unknown' }});
    }});
    rows.sort(function(a, b) {{ return _top20Ascending ? a.score - b.score : b.score - a.score; }});
    var top20 = rows.slice(0, 20);
    _top20Layers = top20.map(function(x) {{ return x.lyr; }});
    var html = '';
    top20.forEach(function(row, i) {{
      html +=
        '<div onclick="flyToTract(' + i + ')"' +
        ' onmouseover="this.style.background=\\'rgba(126,184,212,0.12)\\'"' +
        ' onmouseout="this.style.background=\\'transparent\\'"' +
        ' style="display:flex;align-items:center;gap:8px;padding:6px 4px;cursor:pointer;' +
        'border-bottom:1px solid rgba(255,255,255,0.06);border-radius:4px;transition:background 0.12s;">' +
        '<span style="min-width:22px;font-size:11px;font-weight:700;color:#7eb8d4;text-align:right;">' + (i + 1) + '</span>' +
        '<span style="flex:1;font-size:12px;color:#e8edf3;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding-left:2px;">' + row.label + '</span>' +
        '<span style="font-size:12px;font-weight:600;color:#fecc5c;white-space:nowrap;">' + row.score.toFixed(2) + '</span>' +
        '</div>';
    }});
    var listEl = document.getElementById('top20-list');
    if (listEl) listEl.innerHTML = html;
    var hdr = document.getElementById('top20-header-label');
    if (hdr) hdr.textContent = 'Top 20 · ' + _layerNames[_activeKey];
    var srtBtn = document.getElementById('top20-sort-btn');
    if (srtBtn) srtBtn.textContent = _top20Ascending ? '↑ Low first' : '↓ High first';
  }};

  window.toggleTop20Sort = function() {{
    _top20Ascending = !_top20Ascending;
    buildTop20();
  }};

  window.flyToTract = function(idx) {{
    var map = _getMap();
    if (!map) return;
    if (_inDistrictView) {{
      if (_districtLayer) map.removeLayer(_districtLayer);
      window.{layer_var}.addTo(map);
      _inDistrictView = false;
      _setDistrictBtnState(false);
      _setLayerBtnState(_activeKey);
      _setWeightControlsEnabled(_activeKey === 'ugpi');
      _updateLegend(_activeKey);
    }}
    var lyr = _top20Layers[idx];
    if (!lyr) return;
    var bounds = lyr.getBounds();
    map.flyToBounds(bounds, {{ padding: [60, 60], maxZoom: 16, duration: 0.9 }});
    setTimeout(function() {{ lyr.openPopup(bounds.getCenter()); }}, 1000);
  }};

  window.toggleTop20 = function() {{
    var panel = document.getElementById('top20-panel');
    if (!panel) return;
    panel.style.display = (panel.style.display === 'none' || panel.style.display === '') ? 'block' : 'none';
  }};

  window.switchLayer = function(key) {{
    var map = _getMap();
    if (_inDistrictView && map) {{
      if (_districtLayer) map.removeLayer(_districtLayer);
      window.{layer_var}.addTo(map);
      _inDistrictView = false;
      _setDistrictBtnState(false);
    }}
    _activeKey = key;
    var scale = _scales[key], field = _fields[key];
    window.{layer_var}.eachLayer(function(lyr) {{
      var v = lyr.feature && lyr.feature.properties[field];
      if (v != null) lyr.setStyle({{fillColor: _color(parseFloat(v), scale)}});
    }});
    _setLayerBtnState(key);
    _updateLegend(key);
    _setWeightControlsEnabled(key === 'ugpi');
    buildTop20();
  }};

  window.onWeightSlider = function(changedKey) {{
    var keys = ['heat', 'green', 'social'];
    var s = {{}};
    keys.forEach(function(k) {{ s[k] = document.getElementById('slider-' + k); }});
    var newVal = parseInt(s[changedKey].value);
    var others = keys.filter(function(k) {{ return k !== changedKey; }});
    var o1 = others[0], o2 = others[1];
    var old1 = parseInt(s[o1].value), old2 = parseInt(s[o2].value);
    var oldSum = old1 + old2;
    var remaining = 100 - newVal;
    var new1, new2;
    if (oldSum === 0) {{
      new1 = Math.floor(remaining / 2);
      new2 = remaining - new1;
    }} else {{
      new1 = Math.round(old1 / oldSum * remaining);
      new2 = remaining - new1;
    }}
    s[o1].value = new1;
    s[o2].value = new2;
    document.getElementById('val-heat').textContent   = s['heat'].value   + '%';
    document.getElementById('val-green').textContent  = s['green'].value  + '%';
    document.getElementById('val-social').textContent = s['social'].value + '%';
    document.getElementById('weight-summary').textContent =
      'Heat ' + s['heat'].value + '% · Green ' + s['green'].value + '% · Social ' + s['social'].value + '%';
  }};

  window.recalculateUGPI = function() {{
    var hw = parseInt(document.getElementById('slider-heat').value)   / 100;
    var gw = parseInt(document.getElementById('slider-green').value)  / 100;
    var sw = parseInt(document.getElementById('slider-social').value) / 100;
    window.{layer_var}.eachLayer(function(lyr) {{
      var p = lyr.feature && lyr.feature.properties;
      if (!p) return;
      var h  = parseFloat(p.Heat_Score);
      var g  = parseFloat(p.Green_Space_Deficit_Score);
      var sv = parseFloat(p.Social_Vulnerability_Score);
      if (isNaN(h) || isNaN(g) || isNaN(sv)) return;
      var newUGPI = hw * h + gw * g + sw * sv;
      p.UGPI  = newUGPI;
      p._ugpi = newUGPI.toFixed(2);
      lyr.setStyle({{fillColor: _color(newUGPI, _scales.ugpi)}});
    }});
    _activeKey = 'ugpi';
    _setLayerBtnState('ugpi');
    _updateLegend('ugpi');
    _setWeightControlsEnabled(true);
    _applyFilter();
    buildTop20();
  }};

  window.resetWeights = function() {{
    document.getElementById('slider-heat').value   = 33;
    document.getElementById('slider-green').value  = 33;
    document.getElementById('slider-social').value = 34;
    document.getElementById('val-heat').textContent   = '33%';
    document.getElementById('val-green').textContent  = '33%';
    document.getElementById('val-social').textContent = '34%';
    document.getElementById('weight-summary').textContent = 'Heat 33% \xb7 Green 33% \xb7 Social 34%';
    recalculateUGPI();
  }};

  window.exportCSV = function() {{
    var rows = [['Census Tract','District','UGPI Score','Heat Score','Green Space Deficit Score','Social Vulnerability Score','Mean Temperature C','Mean NDVI','Elderly Population Percent']];
    window.{layer_var}.eachLayer(function(lyr) {{
      var p = lyr.feature && lyr.feature.properties;
      if (!p) return;
      var label   = p.Label || '';
      var parts   = label.split(' \xb7 ');
      var district = parts[0] || '';
      var tract    = parts[1] || '';
      rows.push([
        tract,
        district,
        p._ugpi  || '',
        p._heat  || '',
        p._green || '',
        p._social|| '',
        p._lst   || '',
        p._ndvi  || '',
        p._elderly || ''
      ]);
    }});
    var csv = rows.map(function(r) {{
      return r.map(function(v) {{
        var s = String(v);
        if (s.indexOf(',') !== -1 || s.indexOf('"') !== -1) s = '"' + s.replace(/"/g, '""') + '"';
        return s;
      }}).join(',');
    }}).join('\\n');
    var blob = new Blob([csv], {{type: 'text/csv;charset=utf-8;'}});
    var url  = URL.createObjectURL(blob);
    var a    = document.createElement('a');
    a.href     = url;
    a.download = 'ugpi_barcelona.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }};

  window.toggleSimMode = function() {{
    _simMode = !_simMode;
    _setSimBtnState(_simMode);
    var map = _getMap();
    if (_simMode) {{
      if (map) map.getContainer().style.cursor = 'crosshair';
      _showSimInstruction();
    }} else {{
      if (map) map.getContainer().style.cursor = '';
      _restoreSimStyle();
      _hideSimPanel();
    }}
  }};

  window.closeSimPanel = function() {{
    _restoreSimStyle();
    _hideSimPanel();
    _simMode = false;
    _setSimBtnState(false);
    var map = _getMap();
    if (map) map.getContainer().style.cursor = '';
  }};

  window.onSimSlider = function() {{
    _updateSimPanel();
  }};

  window.shareSimAnalysis = function() {{
    if (!_simLyr || !_simOrigProps) return;
    var p      = _simLyr.feature.properties;
    var dNDVI  = parseFloat(document.getElementById('sim-ndvi').value);
    var dLST   = parseFloat(document.getElementById('sim-lst').value);
    var trees  = Math.round(dNDVI * _simAvgArea / 50);
    var co2    = trees * 22;
    var temp   = Math.round(dNDVI / 0.05 * 0.5 * 10) / 10;
    var pop    = _simOrigProps.pop || 0;
    var text =
      'UGPI Barcelona - Intervention Analysis\\n' +
      'Tract: ' + (p.Label || 'Unknown') + '\\n' +
      'Recommended: ' + _simCurrentRec + '\\n' +
      'NDVI increase: +' + dNDVI.toFixed(2) + '  |  LST reduction: −' + dLST.toFixed(1) + '°C\\n' +
      'Trees required: ≈ ' + trees.toLocaleString() + '\\n' +
      'CO₂ absorbed/yr: ≈ ' + co2.toLocaleString() + ' kg\\n' +
      'Temp. reduction: ' + (temp > 0 ? '−' + temp.toFixed(1) : 'none') + ' °C\\n' +
      'People benefited: ' + (pop > 0 ? pop.toLocaleString() : 'N/A') + '\\n' +
      'Generated by UGPI Barcelona Interactive Map';
    var btn = document.getElementById('sim-share-btn');
    if (navigator.clipboard) {{
      navigator.clipboard.writeText(text).then(function() {{
        if (btn) {{ btn.textContent = '✓ Copied to clipboard!'; setTimeout(function() {{ if (btn) btn.innerHTML = '&#x1F4CB; Share this analysis'; }}, 2000); }}
      }}).catch(function() {{
        if (btn) {{ btn.textContent = 'Copy failed'; setTimeout(function() {{ if (btn) btn.innerHTML = '&#x1F4CB; Share this analysis'; }}, 2000); }}
      }});
    }} else {{
      var ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      try {{ document.execCommand('copy'); }} catch(e) {{}}
      document.body.removeChild(ta);
      if (btn) {{ btn.textContent = '✓ Copied!'; setTimeout(function() {{ if (btn) btn.innerHTML = '&#x1F4CB; Share this analysis'; }}, 2000); }}
    }}
  }};

  window.toggleCompareMode = function() {{
    _compareMode = !_compareMode;
    _setCompareBtnState(_compareMode);
    var map = _getMap();
    if (map) map.getContainer().style.cursor = _compareMode ? 'crosshair' : '';
    if (!_compareMode) {{
      _compareTracts.forEach(function(lyr) {{ _restoreCompareStyle(lyr); }});
      _compareTracts = [];
      _hideComparePanel();
    }}
  }};

  window.clearComparison = function() {{
    _compareTracts.forEach(function(lyr) {{ _restoreCompareStyle(lyr); }});
    _compareTracts = [];
    _hideComparePanel();
  }};

  window.onFilterSlider = function() {{
    var sl = document.getElementById('slider-filter');
    _filterThreshold = parseFloat(sl.value);
    var valEl = document.getElementById('filter-val');
    if (valEl) valEl.textContent = _filterThreshold.toFixed(1);
    _applyFilter();
    buildTop20();
  }};

  window.resetFilter = function() {{
    _filterThreshold = 1.0;
    var sl = document.getElementById('slider-filter');
    if (sl) sl.value = 1;
    var valEl = document.getElementById('filter-val');
    if (valEl) valEl.textContent = '1.0';
    _applyFilter();
    buildTop20();
  }};

  window.hideSearchDropdown = function() {{ _hideDropdown(); }};

  window.onSearchInput = function() {{
    var inp = document.getElementById('search-input');
    var q   = inp ? inp.value.trim() : '';
    var clrBtn = document.getElementById('search-clear');
    if (clrBtn) clrBtn.style.display = q ? 'flex' : 'none';
    if (inp) inp.style.color = '#e8edf3';
    if (_searchDebounceTimer) clearTimeout(_searchDebounceTimer);
    if (q.length < 3) {{ _hideDropdown(); _searchSuggestions = []; return; }}
    _searchDebounceTimer = setTimeout(function() {{
      var url = 'https://nominatim.openstreetmap.org/search?q=' + encodeURIComponent(q) +
                '&format=json&limit=5&countrycodes=es';
      fetch(url, {{ headers: {{ 'Accept-Language': 'en' }} }})
        .then(function(r) {{ return r.json(); }})
        .then(function(data) {{
          _searchSuggestions = data || [];
          _showDropdown(_searchSuggestions);
        }})
        .catch(function() {{ _hideDropdown(); }});
    }}, 300);
  }};

  window.clearSearch = function() {{
    var inp = document.getElementById('search-input');
    if (inp) {{ inp.value = ''; inp.style.color = '#e8edf3'; }}
    var btn = document.getElementById('search-clear');
    if (btn) btn.style.display = 'none';
    if (_searchDebounceTimer) {{ clearTimeout(_searchDebounceTimer); _searchDebounceTimer = null; }}
    _searchSuggestions = [];
    _hideDropdown();
    _clearSearchHighlight();
  }};

  window.searchAddress = function() {{
    _hideDropdown();
    if (_searchSuggestions.length) {{
      var top = _searchSuggestions[0];
      var inp = document.getElementById('search-input');
      if (inp) inp.value = top.display_name;
      var clrBtn = document.getElementById('search-clear');
      if (clrBtn) clrBtn.style.display = 'flex';
      _flyAndHighlight(parseFloat(top.lat), parseFloat(top.lon));
      return;
    }}
    var inp = document.getElementById('search-input');
    var q   = inp ? inp.value.trim() : '';
    if (!q) return;
    var url = 'https://nominatim.openstreetmap.org/search?q=' + encodeURIComponent(q) +
              '&format=json&limit=1&bounded=1' +
              '&viewbox=2.052,41.470,2.228,41.320&countrycodes=es';
    fetch(url, {{ headers: {{ 'Accept-Language': 'en' }} }})
      .then(function(r) {{ return r.json(); }})
      .then(function(data) {{
        if (!data || !data.length) {{
          if (inp) {{
            inp.style.color = '#e05050';
            setTimeout(function() {{ if (inp) inp.style.color = '#e8edf3'; }}, 1500);
          }}
          return;
        }}
        var clrBtn = document.getElementById('search-clear');
        if (clrBtn) clrBtn.style.display = 'flex';
        _flyAndHighlight(parseFloat(data[0].lat), parseFloat(data[0].lon));
      }})
      .catch(function(err) {{ console.error('Geocode error:', err); }});
  }};

  window.addEventListener('load', function() {{
    setTimeout(function() {{
      _map = window.{layer_var}._map;
      _replaceHoverHandlers();
      buildTop20();
      _map.on('click', function() {{ _hideDropdown(); }});
    }}, 400);
  }});

}})();
</script>
"""


SEARCH_BAR_HTML = """
<style>
#search-dropdown li:last-child { border-bottom: none !important; }
#search-input::placeholder { color: #4a6580; }
</style>
<div style="
    position: fixed;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 9999;
    display: flex;
    align-items: stretch;
    gap: 8px;
    font-family: 'Segoe UI', Arial, sans-serif;
">
    <div id="search-container" style="width: 360px; position: relative;">
        <div style="
            display: flex;
            align-items: center;
            background: #1b2838;
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 8px;
            box-shadow: 0 4px 18px rgba(0,0,0,0.50);
            padding: 0 6px 0 12px;
            gap: 4px;
            height: 100%;
            box-sizing: border-box;
            transition: border-color 0.15s;
        ">
            <span style="color:#6b829e; font-size:13px; flex-shrink:0; pointer-events:none;">&#128269;</span>
            <input
                id="search-input"
                type="text"
                placeholder="Search address in Barcelona..."
                autocomplete="off"
                onkeydown="if(event.key==='Enter'){searchAddress();}else if(event.key==='Escape'){clearSearch();}"
                oninput="onSearchInput()"
                onblur="setTimeout(function(){hideSearchDropdown()},160)"
                style="
                    flex: 1;
                    background: transparent;
                    border: none;
                    outline: none;
                    color: #e8edf3;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 12.5px;
                    padding: 10px 2px;
                    min-width: 0;
                "
            >
            <button
                id="search-clear"
                onclick="clearSearch()"
                title="Clear"
                style="
                    display: none;
                    align-items: center;
                    justify-content: center;
                    background: none;
                    border: none;
                    color: #6b829e;
                    cursor: pointer;
                    font-size: 13px;
                    padding: 4px 6px;
                    line-height: 1;
                    flex-shrink: 0;
                    transition: color 0.15s;
                "
                onmouseover="this.style.color='#e8edf3'"
                onmouseout="this.style.color='#6b829e'"
            >&#x2715;</button>
        </div>
        <ul id="search-dropdown" style="
            display: none;
            position: absolute;
            top: calc(100% + 5px);
            left: 0;
            right: 0;
            background: #1b2838;
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 8px;
            box-shadow: 0 8px 28px rgba(0,0,0,0.55);
            list-style: none;
            margin: 0;
            padding: 4px 0;
            overflow: hidden;
        "></ul>
    </div>
    <button onclick="exportCSV()" style="
        background: #1b2838;
        color: #e8edf3;
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 8px;
        padding: 0 14px;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.02em;
        cursor: pointer;
        box-shadow: 0 4px 18px rgba(0,0,0,0.50);
        transition: background 0.15s;
        white-space: nowrap;
        flex-shrink: 0;
    " onmouseover="this.style.background='#243447'" onmouseout="this.style.background='#1b2838'">
        &#11015;&#65039; Export Data
    </button>
    <button onclick="closeWelcomeModal ? openWelcomeModal() : null" id="btn-how-to-use" style="
        background: #1b2838;
        color: #7eb8d4;
        border: 1px solid rgba(126,184,212,0.30);
        border-radius: 8px;
        padding: 0 13px;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 4px 18px rgba(0,0,0,0.50);
        transition: background 0.15s;
        white-space: nowrap;
        flex-shrink: 0;
    " onmouseover="this.style.background='#243447'" onmouseout="this.style.background='#1b2838'"
       onclick="openWelcomeModal()">
        &#9432; How to use
    </button>
</div>
"""

EXPORT_BTN_HTML = ""


DATA_BADGE_HTML = """
<div style="
    position: fixed;
    bottom: 0px;
    left: 260px;
    z-index: 9999;
    background: rgba(255,255,255,0.65);
    color: #505050;
    padding: 2px 6px;
    font-family: 'Helvetica Neue', Arial, Helvetica, sans-serif;
    font-size: 10px;
    line-height: 1.5;
    pointer-events: none;
    white-space: nowrap;
">
    Sentinel-2 and Landsat &middot; Summer 2023 &middot; 1,068 tracts
</div>
"""


WELCOME_MODAL_HTML = """
<style>
@keyframes _ugpiOverlayIn { from { opacity:0; } to { opacity:1; } }
@keyframes _ugpiModalIn   { from { opacity:0; transform:translate(-50%,-47%) scale(0.96); } to { opacity:1; transform:translate(-50%,-50%) scale(1); } }
</style>

<div id="welcome-overlay" style="
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.62);
    z-index: 99998;
    animation: _ugpiOverlayIn 0.30s ease forwards;
" onclick="closeWelcomeModal()"></div>

<div id="welcome-modal" style="
    display: none;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
    z-index: 99999;
    background: #1b2838;
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 16px;
    padding: 38px 42px 34px;
    width: 490px;
    max-width: calc(100vw - 32px);
    box-shadow: 0 28px 72px rgba(0,0,0,0.72);
    font-family: 'Segoe UI', Arial, sans-serif;
    animation: _ugpiModalIn 0.38s cubic-bezier(0.22,0.61,0.36,1) forwards;
">
    <div style="font-size:21px; font-weight:700; color:#ffffff; letter-spacing:0.01em; line-height:1.3; margin-bottom:6px;">
        Urban Greening Priority Index
        <span style="color:#7eb8d4;"> - Barcelona</span>
    </div>
    <div style="font-size:12.5px; color:#5a7898; font-style:italic; margin-bottom:30px;">
        Built for Barcelona city planners, combining satellite imagery, AI and census data into one actionable priority score.
    </div>

    <div style="display:flex; flex-direction:column; gap:20px; margin-bottom:34px;">

        <div style="display:flex; align-items:flex-start; gap:16px;">
            <div style="width:38px; height:38px; border-radius:10px; background:rgba(126,184,212,0.12); border:1px solid rgba(126,184,212,0.22); display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:17px;">&#x1F5FA;&#xFE0F;</div>
            <div>
                <div style="font-size:13px; font-weight:700; color:#e8edf3; margin-bottom:4px;"><span style="color:#7eb8d4;">1.</span> Explore priority zones</div>
                <div style="font-size:12px; color:#5a7898; line-height:1.55;">Each census tract is scored 1-10. Dark red means critical need: heat stress, lack of green space, and vulnerable residents all at once.</div>
            </div>
        </div>

        <div style="display:flex; align-items:flex-start; gap:16px;">
            <div style="width:38px; height:38px; border-radius:10px; background:rgba(126,184,212,0.12); border:1px solid rgba(126,184,212,0.22); display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:17px;">&#x1F39A;&#xFE0F;</div>
            <div>
                <div style="font-size:13px; font-weight:700; color:#e8edf3; margin-bottom:4px;"><span style="color:#7eb8d4;">2.</span> Customize for your goals</div>
                <div style="font-size:12px; color:#5a7898; line-height:1.55;">Adjust how much weight you give to heat, green space, or social vulnerability. The map updates instantly to reflect your planning priorities.</div>
            </div>
        </div>

        <div style="display:flex; align-items:flex-start; gap:16px;">
            <div style="width:38px; height:38px; border-radius:10px; background:rgba(126,184,212,0.12); border:1px solid rgba(126,184,212,0.22); display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:17px;">&#x1F3AF;</div>
            <div>
                <div style="font-size:13px; font-weight:700; color:#e8edf3; margin-bottom:4px;"><span style="color:#7eb8d4;">3.</span> Simulate before you invest</div>
                <div style="font-size:12px; color:#5a7898; line-height:1.55;">Select any tract, model a greening intervention, and instantly see the projected UGPI improvement, trees needed, CO₂ impact, and people benefited.</div>
            </div>
        </div>

    </div>

    <button id="welcome-cta" onclick="closeWelcomeModal()" style="
        display: block;
        width: 100%;
        background: linear-gradient(135deg, #2a6090 0%, #1d4a72 100%);
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: 14px 24px;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.04em;
        cursor: pointer;
        transition: background 0.18s, box-shadow 0.18s;
        box-shadow: 0 4px 20px rgba(42,96,144,0.45);
    " onmouseover="this.style.background='linear-gradient(135deg,#3373a8 0%,#25608e 100%)'"
       onmouseout="this.style.background='linear-gradient(135deg,#2a6090 0%,#1d4a72 100%)'">
        Explore the Map &nbsp;&rarr;
    </button>
</div>

<script>
(function() {
    function _showWelcome() {
        var ov = document.getElementById('welcome-overlay');
        var md = document.getElementById('welcome-modal');
        if (ov) ov.style.display = 'block';
        if (md) md.style.display = 'block';
    }
    function _fadeOut(el) {
        if (!el) return;
        el.style.transition = 'opacity 0.22s';
        el.style.opacity    = '0';
        setTimeout(function() { el.style.display = 'none'; el.style.opacity = ''; el.style.transition = ''; }, 230);
    }
    window.closeWelcomeModal = function() {
        try { localStorage.setItem('ugpi_welcome_v2', '1'); } catch(e) {}
        _fadeOut(document.getElementById('welcome-overlay'));
        _fadeOut(document.getElementById('welcome-modal'));
    };
    window.openWelcomeModal = function() {
        var ov = document.getElementById('welcome-overlay');
        var md = document.getElementById('welcome-modal');
        if (ov) { ov.style.opacity = ''; ov.style.transition = ''; ov.style.display = 'block'; }
        if (md) { md.style.opacity = ''; md.style.transition = ''; md.style.display = 'block'; }
    };
    var seen = false;
    try { seen = !!localStorage.getItem('ugpi_welcome_v2'); } catch(e) {}
    if (!seen) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() { setTimeout(_showWelcome, 250); });
        } else {
            setTimeout(_showWelcome, 250);
        }
    }
})();
</script>
"""


INTERVENTION_PANEL_HTML = """
<div id="sim-panel" style="
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
    font-family: 'Segoe UI', Arial, sans-serif;
">
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; padding-bottom:9px; border-bottom:1px solid rgba(255,255,255,0.10);">
        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.10em; color:#56a85e;">&#x1F331; Intervention Simulator</div>
        <button onclick="closeSimPanel()" style="background:none;border:none;color:#6b829e;cursor:pointer;font-size:14px;padding:2px 5px;line-height:1;transition:color 0.15s;" onmouseover="this.style.color='#e8edf3'" onmouseout="this.style.color='#6b829e'">&#x2715;</button>
    </div>
    <div id="sim-instruction" style="font-size:12px; color:#6b829e; text-align:center; padding:6px 0 2px;">Click a census tract to simulate an intervention</div>
    <div id="sim-tract-label" style="display:none; font-size:12px; font-weight:700; color:#e8edf3; margin-bottom:12px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;"></div>
    <div id="sim-sliders" style="display:none;">
        <div style="margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:3px;">
                <span style="color:#80c080; font-weight:600;">Increase vegetation (NDVI)</span>
                <span style="color:#e8edf3;">+<span id="sim-ndvi-val">0.00</span></span>
            </div>
            <input type="range" id="sim-ndvi" min="0" max="0.20" step="0.01" value="0" oninput="onSimSlider()" style="width:100%; accent-color:#56a85e; cursor:pointer; display:block; margin-bottom:2px;">
            <div style="display:flex; justify-content:space-between; font-size:10px; color:#3a5068;"><span>0</span><span>+0.20</span></div>
        </div>
        <div style="margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:3px;">
                <span style="color:#f0a080; font-weight:600;">Reduce temperature (LST)</span>
                <span style="color:#e8edf3;">&minus;<span id="sim-lst-val">0.0</span>&deg;C</span>
            </div>
            <input type="range" id="sim-lst" min="0" max="3" step="0.1" value="0" oninput="onSimSlider()" style="width:100%; accent-color:#f0a080; cursor:pointer; display:block; margin-bottom:2px;">
            <div style="display:flex; justify-content:space-between; font-size:10px; color:#3a5068;"><span>0&deg;C</span><span>&minus;3&deg;C</span></div>
        </div>
        <div id="sim-scores"></div>
        <div id="sim-trees" style="font-size:11px; color:#80c080; min-height:16px; padding-top:4px;"></div>
        <div id="sim-recommendation"></div>
        <div id="sim-impact"></div>
        <div id="sim-share"></div>
    </div>
</div>
"""

COMPARE_PANEL_HTML = """
<div id="compare-panel" style="
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
    font-family: 'Segoe UI', Arial, sans-serif;
">
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid rgba(255,255,255,0.10);">
        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.10em; color:#7eb8d4;">&#x2696;&#xFE0F; Tract Comparison</div>
        <button onclick="clearComparison()" style="background:rgba(255,255,255,0.07);color:#a0b8cc;border:1px solid rgba(255,255,255,0.12);padding:4px 10px;border-radius:5px;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;font-size:11px;font-weight:600;transition:background 0.15s;" onmouseover="this.style.background='rgba(255,255,255,0.13)'" onmouseout="this.style.background='rgba(255,255,255,0.07)'">Clear Comparison</button>
    </div>
    <div id="compare-content"></div>
</div>
"""


def build_map(gdf: gpd.GeoDataFrame) -> folium.Map:
    b = gdf.total_bounds
    centre = [(b[1] + b[3]) / 2, (b[0] + b[2]) / 2]

    m = folium.Map(location=centre, zoom_start=13, tiles=None)

    folium.TileLayer("CartoDB positron", name="Light (default)", control=True).add_to(m)
    folium.TileLayer("OpenStreetMap",    name="OpenStreetMap",   control=True).add_to(m)

    colormap = cm.LinearColormap(colors=COLORMAP_COLORS, vmin=VMIN, vmax=VMAX)

    popup_fields   = ["Label", "_ugpi", "_heat", "_green", "_social", "_lst", "_ndvi", "_elderly"]
    popup_aliases  = [
        "District · Tract",
        "UGPI Score", "Heat Score", "Green Space Deficit", "Social Vulnerability",
        "Mean Temperature (°C)", "Mean NDVI", "Elderly Population (%)",
    ]

    slim = gdf[popup_fields + ["UGPI", "Heat_Score", "Green_Space_Deficit_Score", "Social_Vulnerability_Score", "total_pop", "geometry"]].copy()

    geojson_layer = folium.GeoJson(
        slim,
        name="UGPI - Census Tracts",
        style_function=lambda feat: {
            "fillColor":   colormap(feat["properties"]["UGPI"]),
            "color":       "white",
            "weight":      0.4,
            "fillOpacity": 0.80,
        },
        highlight_function=lambda feat: {
            "fillColor":   colormap(feat["properties"]["UGPI"]),
            "color":       "#e2e8f0",
            "weight":      2.2,
            "fillOpacity": 0.95,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["Label", "_ugpi"],
            aliases=["District · Tract", "UGPI"],
            style=(
                "font-family:'Segoe UI',Arial,sans-serif;"
                "font-size:13px;"
                "font-weight:500;"
                "background:rgba(27,40,56,0.93);"
                "color:#e8edf3;"
                "border:none;"
                "border-radius:7px;"
                "padding:8px 13px;"
                "box-shadow:0 3px 10px rgba(0,0,0,0.35);"
            ),
            sticky=True,
        ),
        popup=folium.GeoJsonPopup(
            fields=popup_fields,
            aliases=popup_aliases,
            max_width=360,
            style="font-family:'Segoe UI',Arial,sans-serif;font-size:13px;",
            parse_html=False,
            labels=True,
        ),
    )
    geojson_layer.add_to(m)

    ddf = (
        gdf[["District", "UGPI", "Heat_Score", "Green_Space_Deficit_Score", "Social_Vulnerability_Score", "geometry"]]
        .dissolve(by="District", aggfunc="mean")
        .reset_index()
        .sort_values("UGPI", ascending=False)
        .reset_index(drop=True)
    )
    ddf["_rank"] = range(1, len(ddf) + 1)
    district_cols = ["District", "UGPI", "Heat_Score", "Green_Space_Deficit_Score", "Social_Vulnerability_Score", "_rank", "geometry"]
    district_data_js = "<script>var _districtData = " + ddf[district_cols].to_json() + ";</script>"
    m.get_root().html.add_child(bre.Element(district_data_js))

    avg_area_m2  = int(gdf.to_crs(25831).geometry.area.mean())
    ndvi_min     = round(float(gdf["mean_ndvi"].min()), 4)
    ndvi_max     = round(float(gdf["mean_ndvi"].max()), 4)
    lst_min      = round(float(gdf["mean_lst"].min()),  2)
    lst_max      = round(float(gdf["mean_lst"].max()),  2)
    sim_js = (
        f"<script>"
        f"var _simAvgArea={avg_area_m2};"
        f"var _SIM_NDVI_MIN={ndvi_min};var _SIM_NDVI_MAX={ndvi_max};"
        f"var _SIM_LST_MIN={lst_min};var _SIM_LST_MAX={lst_max};"
        f"</script>"
    )
    m.get_root().html.add_child(bre.Element(sim_js))

    m.get_root().html.add_child(bre.Element(SEARCH_BAR_HTML))
    m.get_root().html.add_child(bre.Element(INFO_PANEL_HTML))
    m.get_root().html.add_child(bre.Element(LEGEND_HTML))
    m.get_root().html.add_child(bre.Element(TOP20_PANEL_HTML))
    m.get_root().html.add_child(bre.Element(EXPORT_BTN_HTML))
    m.get_root().html.add_child(bre.Element(INTERVENTION_PANEL_HTML))
    m.get_root().html.add_child(bre.Element(COMPARE_PANEL_HTML))
    m.get_root().html.add_child(bre.Element(DATA_BADGE_HTML))
    m.get_root().html.add_child(bre.Element(WELCOME_MODAL_HTML))
    m.get_root().html.add_child(bre.Element(POPUP_CSS))

    folium.LayerControl(collapsed=False, position="topright").add_to(m)

    m.get_root().html.add_child(bre.Element(
        LAYER_TOGGLE_JS_TEMPLATE.format(layer_var=geojson_layer.get_name())
    ))

    return m


def main() -> None:
    gdf = load_and_prepare()
    m   = build_map(gdf)

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUTS / "ugpi_interactive_map.html"
    m.save(str(out_path))

    size_kb = out_path.stat().st_size // 1024
    print(f"Saved: {out_path}  ({size_kb} KB)")


if __name__ == "__main__":
    main()
