"""Redesign sidebars from dark navy to light grey professional style."""
import re

MAP = 'outputs/ugpi_interactive_map.html'
with open(MAP, 'r', encoding='utf-8') as f:
    m = f.read()

# ── CSS block ──────────────────────────────────────────────────────────────
m = m.replace(
    'background: rgba(126,184,212,0.25); border-radius: 4px; }',
    'background: rgba(0,0,0,0.15); border-radius: 4px; }'
)
m = m.replace(
    '#left-sidebar input[type=range] { -webkit-appearance: none; height: 3px; border-radius: 2px; background: rgba(255,255,255,0.12); outline: none; border: none; }',
    '#left-sidebar input[type=range] { -webkit-appearance: none; height: 5px; border-radius: 3px; background: rgba(0,0,0,0.10); outline: none; border: none; }'
)
m = m.replace(
    '#search-input::placeholder { color: #4a6580; }',
    '#search-input::placeholder { color: #9aa3af; }'
)

# ── Left sidebar container ─────────────────────────────────────────────────
m = m.replace(
    '    background: #1b2838;\n    border-right: 1px solid rgba(255,255,255,0.10);',
    '    background: #f2f4f7;\n    border-right: 1px solid rgba(0,0,0,0.08);'
)

# ── Left sidebar header ────────────────────────────────────────────────────
m = m.replace(
    'font-size:13.5px; font-weight:700; letter-spacing:0.01em; color:#ffffff; line-height:1.3; margin-bottom:3px;',
    'font-size:13.5px; font-weight:700; letter-spacing:0.01em; color:#1a2535; line-height:1.3; margin-bottom:3px;'
)
m = m.replace(
    'font-size:10.5px; color:#4a6580; margin-bottom:14px; line-height:1.4; letter-spacing:0.01em;',
    'font-size:10.5px; color:#8d97a5; margin-bottom:14px; line-height:1.4; letter-spacing:0.01em;'
)
m = m.replace(
    'height:1px; background:rgba(255,255,255,0.10); margin-bottom:0;',
    'height:1px; background:rgba(0,0,0,0.07); margin-bottom:0;'
)

# ── Search box ─────────────────────────────────────────────────────────────
m = m.replace(
    'background:rgba(255,255,255,0.06);\n                border:1px solid rgba(255,255,255,0.12);',
    'background:rgba(0,0,0,0.04);\n                border:1px solid rgba(0,0,0,0.10);'
)
m = m.replace(
    'stroke="#4a6580" stroke-width="2.5" stroke-linecap="round"><circle cx="11"',
    'stroke="#9aa3af" stroke-width="2.5" stroke-linecap="round"><circle cx="11"'
)
m = m.replace(
    'color:#e8edf3; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;\n                        font-size:11.5px; padding:8px 2px; min-width:0;',
    'color:#1a2535; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;\n                        font-size:11.5px; padding:8px 2px; min-width:0;'
)
# search clear button
m = m.replace(
    'background:none;border:none;color:#6b829e;cursor:pointer;font-size:12px;padding:2px 4px;line-height:1;flex-shrink:0;transition:color 0.15s;',
    'background:none;border:none;color:#9aa3af;cursor:pointer;font-size:12px;padding:2px 4px;line-height:1;flex-shrink:0;transition:color 0.15s;'
)
m = m.replace(
    'onmouseover="this.style.color=\'#e8edf3\'" onmouseout="this.style.color=\'#6b829e\'"',
    'onmouseover="this.style.color=\'#1a2535\'" onmouseout="this.style.color=\'#9aa3af\'"'
)
m = m.replace(
    'background:#1b2838; border:1px solid rgba(255,255,255,0.15);\n                border-radius:7px; box-shadow:0 8px 28px rgba(0,0,0,0.55);',
    'background:#ffffff; border:1px solid rgba(0,0,0,0.10);\n                border-radius:7px; box-shadow:0 8px 28px rgba(0,0,0,0.15);'
)

# ── Section dividers and labels ────────────────────────────────────────────
# Section border-top lines in left sidebar
m = m.replace(
    'border-top:1px solid rgba(255,255,255,0.10); padding-top:12px; margin-top:12px; margin-bottom:0;',
    'border-top:1px solid rgba(0,0,0,0.07); padding-top:12px; margin-top:12px; margin-bottom:0;'
)
m = m.replace(
    'border-top:1px solid rgba(255,255,255,0.10); padding-top:12px; margin-top:12px;">',
    'border-top:1px solid rgba(0,0,0,0.07); padding-top:12px; margin-top:12px;">'
)
m = m.replace(
    'border-top:1px solid rgba(255,255,255,0.08); padding-top:10px; margin-top:10px;',
    'border-top:1px solid rgba(0,0,0,0.07); padding-top:10px; margin-top:10px;'
)
# weight-section border
m = m.replace(
    '<div id="weight-section" style="border-top:1px solid rgba(255,255,255,0.10); padding-top:12px; margin-top:12px;">',
    '<div id="weight-section" style="border-top:1px solid rgba(0,0,0,0.07); padding-top:12px; margin-top:12px;">'
)
# priority filter border
m = m.replace(
    'border-top:1px solid rgba(255,255,255,0.10); padding-top:12px; margin-top:12px; margin-bottom:12px;',
    'border-top:1px solid rgba(0,0,0,0.07); padding-top:12px; margin-top:12px; margin-bottom:12px;'
)
# bottom actions border
m = m.replace(
    'padding:10px 16px 14px; border-top:1px solid rgba(255,255,255,0.10); flex-shrink:0; display:flex; gap:6px;',
    'padding:10px 16px 14px; border-top:1px solid rgba(0,0,0,0.07); flex-shrink:0; display:flex; gap:6px;'
)

# Section labels (UPPERCASE grey labels)
m = m.replace(
    'font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:rgba(255,255,255,0.30); margin-bottom:9px;',
    'font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#9aa3af; margin-bottom:9px;'
)
m = m.replace(
    'font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:rgba(255,255,255,0.30); margin-bottom:8px;',
    'font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#9aa3af; margin-bottom:8px;'
)
m = m.replace(
    'font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:rgba(255,255,255,0.30); margin-bottom:10px;',
    'font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#9aa3af; margin-bottom:10px;'
)

# ── Data Layers dots & text ────────────────────────────────────────────────
m = m.replace(
    'font-size:11px; color:rgba(255,255,255,0.65); font-weight:500;">Heat <span style="color:rgba(255,255,255,0.28); font-weight:400;">· Land Surface Temperature</span>',
    'font-size:11px; color:#3d4a58; font-weight:500;">Heat <span style="color:#9aa3af; font-weight:400;">· Land Surface Temperature</span>'
)
m = m.replace(
    'font-size:11px; color:rgba(255,255,255,0.65); font-weight:500;">Green Space Deficit <span style="color:rgba(255,255,255,0.28); font-weight:400;">· NDVI</span>',
    'font-size:11px; color:#3d4a58; font-weight:500;">Green Space Deficit <span style="color:#9aa3af; font-weight:400;">· NDVI</span>'
)
m = m.replace(
    'font-size:11px; color:rgba(255,255,255,0.65); font-weight:500;">Social Vulnerability <span style="color:rgba(255,255,255,0.28); font-weight:400;">· Elderly + income</span>',
    'font-size:11px; color:#3d4a58; font-weight:500;">Social Vulnerability <span style="color:#9aa3af; font-weight:400;">· Elderly + income</span>'
)
m = m.replace(
    'margin-top:8px; font-size:9.5px; color:rgba(255,255,255,0.18); letter-spacing:0.01em;',
    'margin-top:8px; font-size:9.5px; color:#b0bac5; letter-spacing:0.01em;'
)

# ── Map Layer buttons ──────────────────────────────────────────────────────
# Active button (UGPI - starts active)
m = m.replace(
    '<button id="btn-ugpi"   onclick="switchLayer(\'ugpi\')"   style="background:rgba(255,255,255,0.88);color:#1b2838;border:1px solid transparent;padding:9px 8px;border-radius:6px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11px;font-weight:600;text-align:center;transition:all 0.15s;letter-spacing:0.01em;">UGPI</button>',
    '<button id="btn-ugpi"   onclick="switchLayer(\'ugpi\')"   style="background:#1a2535;color:#ffffff;border:1px solid transparent;padding:9px 8px;border-radius:6px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11px;font-weight:700;text-align:center;transition:all 0.15s;letter-spacing:0.01em;box-shadow:0 2px 6px rgba(0,0,0,0.18);">UGPI</button>'
)
# Inactive buttons
m = m.replace(
    '<button id="btn-heat"   onclick="switchLayer(\'heat\')"   style="background:rgba(255,255,255,0.05);color:rgba(255,255,255,0.45);border:1px solid rgba(255,255,255,0.08);padding:9px 8px;border-radius:6px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11px;font-weight:400;text-align:center;transition:all 0.15s;">Heat</button>',
    '<button id="btn-heat"   onclick="switchLayer(\'heat\')"   style="background:#ffffff;color:#6b7789;border:1px solid rgba(0,0,0,0.10);padding:9px 8px;border-radius:6px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11px;font-weight:400;text-align:center;transition:all 0.15s;">Heat</button>'
)
m = m.replace(
    '<button id="btn-green"  onclick="switchLayer(\'green\')"  style="background:rgba(255,255,255,0.05);color:rgba(255,255,255,0.45);border:1px solid rgba(255,255,255,0.08);padding:9px 8px;border-radius:6px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11px;font-weight:400;text-align:center;transition:all 0.15s;">Green Deficit</button>',
    '<button id="btn-green"  onclick="switchLayer(\'green\')"  style="background:#ffffff;color:#6b7789;border:1px solid rgba(0,0,0,0.10);padding:9px 8px;border-radius:6px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11px;font-weight:400;text-align:center;transition:all 0.15s;">Green Deficit</button>'
)
m = m.replace(
    '<button id="btn-social" onclick="switchLayer(\'social\')" style="background:rgba(255,255,255,0.05);color:rgba(255,255,255,0.45);border:1px solid rgba(255,255,255,0.08);padding:9px 8px;border-radius:6px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11px;font-weight:400;text-align:center;transition:all 0.15s;">Social Vuln.</button>',
    '<button id="btn-social" onclick="switchLayer(\'social\')" style="background:#ffffff;color:#6b7789;border:1px solid rgba(0,0,0,0.10);padding:9px 8px;border-radius:6px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11px;font-weight:400;text-align:center;transition:all 0.15s;">Social Vuln.</button>'
)

# ── Analysis Tools buttons ─────────────────────────────────────────────────
m = m.replace(
    '<button id="btn-district" onclick="toggleDistrictView()" style="background:transparent;color:rgba(255,255,255,0.45);border:1px solid rgba(255,255,255,0.07);padding:8px 12px;border-radius:5px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11px;font-weight:400;text-align:left;transition:all 0.15s;width:100%;">District View</button>',
    '<button id="btn-district" onclick="toggleDistrictView()" style="background:transparent;color:#6b7789;border:1px solid rgba(0,0,0,0.08);padding:8px 12px;border-radius:5px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11px;font-weight:400;text-align:left;transition:all 0.15s;width:100%;">District View</button>'
)
m = m.replace(
    '<button id="btn-compare" onclick="toggleCompareMode()" style="background:transparent;color:rgba(255,255,255,0.45);border:1px solid rgba(255,255,255,0.07);padding:8px 12px;border-radius:5px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11px;font-weight:400;text-align:left;transition:all 0.15s;width:100%;">Compare Tracts</button>',
    '<button id="btn-compare" onclick="toggleCompareMode()" style="background:transparent;color:#6b7789;border:1px solid rgba(0,0,0,0.08);padding:8px 12px;border-radius:5px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11px;font-weight:400;text-align:left;transition:all 0.15s;width:100%;">Compare Tracts</button>'
)
m = m.replace(
    '<button id="btn-sim" onclick="toggleSimMode()" style="background:transparent;color:rgba(255,255,255,0.45);border:1px solid rgba(255,255,255,0.07);padding:8px 12px;border-radius:5px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11px;font-weight:400;text-align:left;transition:all 0.15s;width:100%;">Simulate Intervention</button>',
    '<button id="btn-sim" onclick="toggleSimMode()" style="background:transparent;color:#6b7789;border:1px solid rgba(0,0,0,0.08);padding:8px 12px;border-radius:5px;cursor:pointer;font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;font-size:11px;font-weight:400;text-align:left;transition:all 0.15s;width:100%;">Simulate Intervention</button>'
)

# ── Adjust Weights labels ──────────────────────────────────────────────────
# Fix social vulnerability overflow + update all label colors
m = m.replace(
    '<span style="color:#f0a080; font-weight:600;">Heat</span>\n                    <span id="val-heat" style="color:#e8edf3;">33%</span>',
    '<span style="color:#c0614a; font-weight:600; flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; padding-right:6px;">Heat</span>\n                    <span id="val-heat" style="color:#4b5668; flex-shrink:0;">33%</span>'
)
m = m.replace(
    '<span style="color:#80c080; font-weight:600;">Green Space</span>\n                    <span id="val-green" style="color:#e8edf3;">33%</span>',
    '<span style="color:#3a8040; font-weight:600; flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; padding-right:6px;">Green Space</span>\n                    <span id="val-green" style="color:#4b5668; flex-shrink:0;">33%</span>'
)
m = m.replace(
    '<span style="color:#9ab4e0; font-weight:600;">Social Vulnerability</span>\n                    <span id="val-social" style="color:#e8edf3;">34%</span>',
    '<span style="color:#3a6aaa; font-weight:600; flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; padding-right:6px;">Social Vulnerability</span>\n                    <span id="val-social" style="color:#4b5668; flex-shrink:0;">34%</span>'
)
# Weight summary
m = m.replace(
    '<div id="weight-summary" style="font-size:10px; color:#3d5268; text-align:center; margin-bottom:8px;">',
    '<div id="weight-summary" style="font-size:10px; color:#9aa3af; text-align:center; margin-bottom:8px;">'
)
# Reset button
m = m.replace(
    'flex:0 0 auto; background:rgba(255,255,255,0.05); color:#a0b8cc; border:1px solid rgba(255,255,255,0.09); padding:7px 11px; border-radius:5px; cursor:pointer; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif; font-size:11.5px; font-weight:600; transition:background 0.15s;">Reset</button>',
    'flex:0 0 auto; background:#ffffff; color:#4b5668; border:1px solid rgba(0,0,0,0.10); padding:7px 11px; border-radius:5px; cursor:pointer; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif; font-size:11.5px; font-weight:600; transition:background 0.15s;">Reset</button>'
)
# Recalculate button
m = m.replace(
    'flex:1; background:rgba(126,184,212,0.12); color:#e8edf3; border:1px solid rgba(126,184,212,0.35); padding:7px 12px; border-radius:5px; cursor:pointer; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif; font-size:11.5px; font-weight:600; transition:background 0.15s; letter-spacing:0.01em;">Recalculate</button>',
    'flex:1; background:#1a2535; color:#ffffff; border:1px solid transparent; padding:7px 12px; border-radius:5px; cursor:pointer; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif; font-size:11.5px; font-weight:600; transition:background 0.15s; letter-spacing:0.01em; box-shadow:0 2px 5px rgba(0,0,0,0.14);">Recalculate</button>'
)

# ── Priority Filter ────────────────────────────────────────────────────────
m = m.replace(
    '<span style="color:#c8d6e5;">Show tracts with UGPI &ge;</span>\n                <span id="filter-val" style="color:#e8edf3; font-weight:600;">1.0</span>',
    '<span style="color:#4b5668;">Show tracts with UGPI &ge;</span>\n                <span id="filter-val" style="color:#1a2535; font-weight:600;">1.0</span>'
)
m = m.replace(
    '<span id="filter-counter" style="font-size:10px; color:#3d5268;">1068 of 1068 tracts above threshold</span>',
    '<span id="filter-counter" style="font-size:10px; color:#9aa3af;">1068 of 1068 tracts above threshold</span>'
)
# Show All button
m = m.replace(
    'flex:0 0 auto; background:rgba(255,255,255,0.05); color:#a0b8cc; border:1px solid rgba(255,255,255,0.09); padding:3px 9px; border-radius:5px; cursor:pointer; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif; font-size:11px; font-weight:600; white-space:nowrap; transition:background 0.15s;">Show All</button>',
    'flex:0 0 auto; background:#ffffff; color:#4b5668; border:1px solid rgba(0,0,0,0.10); padding:3px 9px; border-radius:5px; cursor:pointer; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif; font-size:11px; font-weight:600; white-space:nowrap; transition:background 0.15s;">Show All</button>'
)

# ── Bottom action buttons ──────────────────────────────────────────────────
m = m.replace(
    'flex:1; background:rgba(255,255,255,0.05); color:#a0b8cc;\n            border:1px solid rgba(255,255,255,0.09); border-radius:5px;\n            padding:8px 10px; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;\n            font-size:11.5px; font-weight:600; cursor:pointer;\n            transition:background 0.15s; white-space:nowrap;\n        " onmouseover="this.style.background=\'rgba(255,255,255,0.10)\'" onmouseout="this.style.background=\'rgba(255,255,255,0.05)\'">',
    'flex:1; background:#ffffff; color:#4b5668;\n            border:1px solid rgba(0,0,0,0.10); border-radius:5px;\n            padding:8px 10px; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;\n            font-size:11.5px; font-weight:600; cursor:pointer;\n            transition:background 0.15s; white-space:nowrap;\n        " onmouseover="this.style.background=\'#f5f6f8\'" onmouseout="this.style.background=\'#ffffff\'">'
)
m = m.replace(
    'flex:1; background:rgba(126,184,212,0.07); color:#7eb8d4;\n            border:1px solid rgba(126,184,212,0.22); border-radius:5px;\n            padding:8px 10px; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;\n            font-size:11.5px; font-weight:600; cursor:pointer;\n            transition:background 0.15s; white-space:nowrap;\n        " onmouseover="this.style.background=\'rgba(126,184,212,0.14)\'" onmouseout="this.style.background=\'rgba(126,184,212,0.07)\'">',
    'flex:1; background:#1a2535; color:#ffffff;\n            border:1px solid transparent; border-radius:5px;\n            padding:8px 10px; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif;\n            font-size:11.5px; font-weight:600; cursor:pointer;\n            transition:background 0.15s; white-space:nowrap; box-shadow:0 2px 5px rgba(0,0,0,0.14);\n        " onmouseover="this.style.background=\'#2d3d52\'" onmouseout="this.style.background=\'#1a2535\'">'
)

# ── Right sidebar container ────────────────────────────────────────────────
m = m.replace(
    '    background: #1b2838;\n    border-left: 1px solid rgba(255,255,255,0.10);',
    '    background: #f2f4f7;\n    border-left: 1px solid rgba(0,0,0,0.08);'
)
# Right sidebar section borders
m = m.replace(
    'padding:18px 18px 14px; flex-shrink:0; border-bottom:1px solid rgba(255,255,255,0.10);',
    'padding:18px 18px 14px; flex-shrink:0; border-bottom:1px solid rgba(0,0,0,0.07);'
)
m = m.replace(
    'padding:14px 18px 10px; flex-shrink:0; border-bottom:1px solid rgba(255,255,255,0.10);',
    'padding:14px 18px 10px; flex-shrink:0; border-bottom:1px solid rgba(0,0,0,0.07);'
)
# Legend label
m = m.replace(
    'font-size:9px; font-weight:700; text-transform:uppercase;\n            letter-spacing:0.13em; color:#7eb8d4; margin-bottom:10px;',
    'font-size:9px; font-weight:700; text-transform:uppercase;\n            letter-spacing:0.13em; color:#2d6fb0; margin-bottom:10px;'
)
# Legend lo/hi text
m = m.replace(
    'display:flex; justify-content:space-between; font-size:10px; color:#4a6580;',
    'display:flex; justify-content:space-between; font-size:10px; color:#8d97a5;'
)
# District Rankings label
m = m.replace(
    'font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#7eb8d4; margin-bottom:9px;">District Rankings</div>',
    'font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#2d6fb0; margin-bottom:9px;">District Rankings</div>'
)
# Top20 header label + sort button
m = m.replace(
    '<span id="top20-header-label" style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#7eb8d4;">Top 20 &middot; UGPI</span>',
    '<span id="top20-header-label" style="font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.13em; color:#2d6fb0;">Top 20 &middot; UGPI</span>'
)
m = m.replace(
    'font-size:10px; font-weight:600; color:#7eb8d4; background:transparent; border:1px solid rgba(126,184,212,0.28); border-radius:4px; padding:2px 6px; cursor:pointer; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif; white-space:nowrap; transition:all 0.15s;">High first</button>',
    'font-size:10px; font-weight:600; color:#2d6fb0; background:#ffffff; border:1px solid rgba(45,111,176,0.25); border-radius:4px; padding:2px 6px; cursor:pointer; font-family:\'Inter\',\'Segoe UI\',Arial,sans-serif; white-space:nowrap; transition:all 0.15s;">High first</button>'
)
# Top20 column header row
m = m.replace(
    'display:flex; font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#2d4055; padding:3px 2px 5px; border-bottom:1px solid rgba(255,255,255,0.07); margin-bottom:3px; flex-shrink:0;',
    'display:flex; font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#9aa3af; padding:3px 2px 5px; border-bottom:1px solid rgba(0,0,0,0.07); margin-bottom:3px; flex-shrink:0;'
)
# Attribution
m = m.replace(
    'padding:7px 18px 10px; border-top:1px solid rgba(255,255,255,0.06); flex-shrink:0;',
    'padding:7px 18px 10px; border-top:1px solid rgba(0,0,0,0.06); flex-shrink:0;'
)
m = m.replace(
    'font-size:9px; color:#2d4055; line-height:1.5; letter-spacing:0.01em;',
    'font-size:9px; color:#9aa3af; line-height:1.5; letter-spacing:0.01em;'
)

# ── JS: buildTop20 row colors ──────────────────────────────────────────────
m = m.replace(
    "'border-bottom:1px solid rgba(255,255,255,0.06);border-radius:4px;transition:background 0.12s;\">'",
    "'border-bottom:1px solid rgba(0,0,0,0.06);border-radius:4px;transition:background 0.12s;\">' "
)
# rank number color
m = m.replace(
    "style=\"min-width:22px;font-size:11px;font-weight:700;color:#7eb8d4;text-align:right;\">' + (i + 1) + '</span>'",
    "style=\"min-width:22px;font-size:11px;font-weight:700;color:#2d6fb0;text-align:right;\">' + (i + 1) + '</span>'"
)
# tract label color
m = m.replace(
    "style=\"flex:1;font-size:12px;color:#e8edf3;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding-left:2px;\">'",
    "style=\"flex:1;font-size:12px;color:#1a2535;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding-left:2px;\">' "
)
# score color
m = m.replace(
    "style=\"font-size:12px;font-weight:600;color:#fecc5c;white-space:nowrap;\">' + row.score.toFixed(2) + '</span>'",
    "style=\"font-size:12px;font-weight:600;color:#c0614a;white-space:nowrap;\">' + row.score.toFixed(2) + '</span>'"
)
# hover state
m = m.replace(
    "onmouseover=\"this.style.background='rgba(126,184,212,0.12)'\"",
    "onmouseover=\"this.style.background='rgba(0,0,0,0.04)'\""
)

# ── JS: buildDistrictRanking row colors ───────────────────────────────────
m = m.replace(
    "var bg = i % 2 === 0 ? 'rgba(255,255,255,0.02)' : 'transparent';",
    "var bg = i % 2 === 0 ? 'rgba(0,0,0,0.025)' : 'transparent';"
)
m = m.replace(
    "style=\"min-width:16px;font-size:9.5px;font-weight:700;color:#2d4055;\">' + (i+1) + '</span>'",
    "style=\"min-width:16px;font-size:9.5px;font-weight:700;color:#9aa3af;\">' + (i+1) + '</span>'"
)
m = m.replace(
    "style=\"flex:1;font-size:10.5px;color:#c8d6e5;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;\">' + d.name + '</span>'",
    "style=\"flex:1;font-size:10.5px;color:#3d4a58;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;\">' + d.name + '</span>'"
)

# ── JS: _setLayerBtnState ──────────────────────────────────────────────────
m = m.replace(
    "      btn.style.background  = on ? 'rgba(255,255,255,0.88)' : 'rgba(255,255,255,0.05)';\n      btn.style.color       = on ? '#1b2838'                : 'rgba(255,255,255,0.45)';\n      btn.style.borderColor = on ? 'transparent'            : 'rgba(255,255,255,0.08)';\n      btn.style.fontWeight  = on ? '600'                    : '400';",
    "      btn.style.background  = on ? '#1a2535'             : '#ffffff';\n      btn.style.color       = on ? '#ffffff'               : '#6b7789';\n      btn.style.borderColor = on ? 'transparent'           : 'rgba(0,0,0,0.10)';\n      btn.style.fontWeight  = on ? '700'                   : '400';\n      btn.style.boxShadow   = on ? '0 2px 6px rgba(0,0,0,0.18)' : 'none';"
)

# ── JS: _setDistrictBtnState ───────────────────────────────────────────────
m = m.replace(
    "    btn.style.background  = active ? 'rgba(126,184,212,0.14)' : 'transparent';\n    btn.style.color       = active ? '#7eb8d4'                : 'rgba(255,255,255,0.45)';\n    btn.style.borderColor = active ? 'rgba(126,184,212,0.35)' : 'rgba(255,255,255,0.07)';\n    btn.style.fontWeight  = active ? '600'                    : '400';",
    "    btn.style.background  = active ? 'rgba(45,111,176,0.10)'  : 'transparent';\n    btn.style.color       = active ? '#2d6fb0'                : '#6b7789';\n    btn.style.borderColor = active ? 'rgba(45,111,176,0.28)'  : 'rgba(0,0,0,0.08)';\n    btn.style.fontWeight  = active ? '600'                    : '400';"
)

# ── JS: _setCompareBtnState ────────────────────────────────────────────────
m = m.replace(
    "    btn.style.background  = active ? 'rgba(254,204,92,0.14)'  : 'transparent';\n    btn.style.color       = active ? '#fecc5c'                : 'rgba(255,255,255,0.45)';\n    btn.style.borderColor = active ? 'rgba(254,204,92,0.35)'  : 'rgba(255,255,255,0.07)';\n    btn.style.fontWeight  = active ? '600'                    : '400';",
    "    btn.style.background  = active ? 'rgba(160,120,40,0.10)'  : 'transparent';\n    btn.style.color       = active ? '#9a7828'                : '#6b7789';\n    btn.style.borderColor = active ? 'rgba(160,120,40,0.28)'  : 'rgba(0,0,0,0.08)';\n    btn.style.fontWeight  = active ? '600'                    : '400';"
)

# ── JS: _setSimBtnState ────────────────────────────────────────────────────
m = m.replace(
    "    btn.style.background  = active ? 'rgba(86,168,94,0.14)'   : 'transparent';\n    btn.style.color       = active ? '#80c080'                : 'rgba(255,255,255,0.45)';\n    btn.style.borderColor = active ? 'rgba(86,168,94,0.35)'   : 'rgba(255,255,255,0.07)';\n    btn.style.fontWeight  = active ? '600'                    : '400';",
    "    btn.style.background  = active ? 'rgba(42,118,52,0.10)'   : 'transparent';\n    btn.style.color       = active ? '#2a7634'                : '#6b7789';\n    btn.style.borderColor = active ? 'rgba(42,118,52,0.28)'   : 'rgba(0,0,0,0.08)';\n    btn.style.fontWeight  = active ? '600'                    : '400';"
)

with open(MAP, 'w', encoding='utf-8') as f:
    f.write(m)

print("Sidebar light theme applied.")
