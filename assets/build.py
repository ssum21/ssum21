"""Generate the profile README header and card SVGs in light and dark themes.

Run from this directory: python3 build.py
"""
from __future__ import annotations

import random
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent

THEMES = {
    "light": {
        "bg": "#fbfbf9",
        "card": "#ffffff",
        "text": "#1f2328",
        "sub": "#2d3439",
        "muted": "#6e7781",
        "border": "#e3e5e8",
        "accent": "#3a6ea5",
        "cell": "#2d3439",
    },
    "dark": {
        "bg": "#0d1117",
        "card": "#161b22",
        "text": "#e6edf3",
        "sub": "#c9d1d9",
        "muted": "#8b949e",
        "border": "#30363d",
        "accent": "#7aa2f7",
        "cell": "#c9d1d9",
    },
}

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

PHRASES = [
    "KV-cache eviction for long-context LLMs",
    "efficient LLM inference",
    "on-device and multimodal AI",
]


def header(t: dict[str, str]) -> str:
    """Hero banner: name block on the left, animated KV-cache grid on the right."""
    w, h = 880, 240
    rows, cols, size, gap = 6, 14, 14, 5
    gx, gy = 560, 52
    rng = random.Random(21)
    cells = []
    for r in range(rows):
        for c in range(cols):
            x = gx + c * (size + gap)
            y = gy + r * (size + gap)
            evicted = rng.random() < 0.38 and c < cols - 2
            delay = round(rng.uniform(0, 4.5), 2)
            anim = (
                '<animate attributeName="opacity" values=".82;.82;.08;.08;.82" '
                f'keyTimes="0;.35;.5;.85;1" dur="6s" begin="{delay}s" repeatCount="indefinite"/>'
                if evicted
                else ""
            )
            cells.append(
                f'<rect class="cell" x="{x}" y="{y}" width="{size}" height="{size}" rx="3" opacity=".82">{anim}</rect>'
            )
    grid_w = cols * (size + gap) - gap
    grid_h = rows * (size + gap) - gap
    n = len(PHRASES)
    period = 3 * n
    step = 1 / n
    phrase_nodes = [
        f'<text class="phrase" x="40" y="186" opacity="0">{escape(p)}'
        f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.04;{step - .04:.3f};{step:.3f};1" '
        f'dur="{period}s" begin="{3 * i}s" repeatCount="indefinite"/></text>'
        for i, p in enumerate(PHRASES)
    ]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Sumin Im, AI Systems and Research Engineer, M.S. student at KAIST EE">
  <style>
    .label {{ font: 600 12px {MONO}; letter-spacing: 3px; fill: {t["muted"]}; }}
    .name {{ font: 700 44px {SANS}; fill: {t["text"]}; }}
    .kr {{ font: 500 20px {SANS}; fill: {t["muted"]}; }}
    .role {{ font: 500 17px {SANS}; fill: {t["sub"]}; }}
    .now {{ font: 600 12px {MONO}; letter-spacing: 2px; fill: {t["accent"]}; }}
    .phrase {{ font: 500 17px {SANS}; fill: {t["text"]}; }}
    .caption {{ font: 500 11px {MONO}; fill: {t["muted"]}; }}
    .cell {{ fill: {t["cell"]}; }}
    .scan {{ fill: {t["accent"]}; opacity: .18; }}
  </style>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="{t["bg"]}" stroke="{t["border"]}"/>
  <text class="label" x="40" y="54">SUMIN.IM</text>
  <text class="name" x="40" y="106">Sumin Im <tspan class="kr" dx="6">임수민</tspan></text>
  <text class="role" x="40" y="138">AI Systems &amp; Research Engineer · M.S. Student, KAIST EE</text>
  <text class="now" x="40" y="164">NOW WORKING ON</text>
  {"".join(phrase_nodes)}
  <g>
    {"".join(cells)}
    <rect class="scan" x="{gx}" y="{gy - 6}" width="14" height="{grid_h + 12}" rx="4"><animate attributeName="x" values="{gx};{gx + grid_w - 14}" dur="6s" repeatCount="indefinite"/></rect>
  </g>
  <text class="caption" x="{gx}" y="{gy + grid_h + 26}">kv cache · layers × tokens · keep / evict</text>
</svg>
'''


CARDS = [
    ("now", "NOW", "KV-cache eviction", ["Efficient LLM inference at KAIST MIIL", "Advised by Prof. Sung-Ju Lee"], "sumin.im"),
    ("oss", "OPEN SOURCE", "Hugging Face Transformers", ["4 merged Korean docs", "DeepSeek-V3 · BigBird · X-CLIP · LFM2"], "merged PRs"),
    ("bench", "BENCHMARK", "Ko-AgentBench", ["Korean agentic tool-calling benchmark", "with Hugging Face KREW"], "repository"),
    ("writing", "WRITING", "Research notes", ["Paper reviews on KV cache, test-time", "scaling, and LLM reasoning"], "sumin.im/blog"),
    ("pubs", "PUBLICATIONS", "2 papers · 2 patents", ["KSGIS 2025 · KIISE 2024", "On-device AI security (pending)"], "sumin.im"),
    ("honors", "HONORS", "President Award · Grand Prize", ["AI MCP Hackathon, 2nd of 47 teams", "UNI-DTHON, 1st of 140"], "sumin.im"),
]


def card(t: dict[str, str], label: str, title: str, lines: list[str], link: str) -> str:
    """One info card. The README wraps it in a link."""
    w, h = 420, 150
    body = "".join(
        f'<text class="line" x="24" y="{94 + 20 * i}">{escape(s)}</text>' for i, s in enumerate(lines)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}: {escape(title)}">
  <style>
    .label {{ font: 600 11px {MONO}; letter-spacing: 2.5px; fill: {t["accent"]}; }}
    .title {{ font: 700 20px {SANS}; fill: {t["text"]}; }}
    .line {{ font: 400 14px {SANS}; fill: {t["muted"]}; }}
    .link {{ font: 500 11px {MONO}; fill: {t["muted"]}; }}
    .dot {{ fill: {t["accent"]}; }}
  </style>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>
  <circle class="dot" cx="{w - 28}" cy="30" r="4"><animate attributeName="opacity" values="1;.25;1" dur="2.4s" repeatCount="indefinite"/></circle>
  <text class="label" x="24" y="34">{escape(label)}</text>
  <text class="title" x="24" y="64">{escape(title)}</text>
  {body}
  <text class="link" x="{w - 24}" y="{h - 16}" text-anchor="end">{escape(link)} →</text>
</svg>
'''


def main() -> None:
    for name, t in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(header(t), encoding="utf-8")
        for key, label, title, lines, link in CARDS:
            (OUT / f"card-{key}-{name}.svg").write_text(card(t, label, title, lines, link), encoding="utf-8")


if __name__ == "__main__":
    main()
