#!/usr/bin/env python3
"""
AI Radar PDF Generator

Reads a JSON report file and generates a premium PDF in clean
Apple/Notion/Linear/Stripe aesthetic.

Uses Chrome headless to render HTML → PDF (no Python dependencies needed).

Usage:
    python3 generate_pdf.py --input report.json --output report.pdf
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from datetime import datetime


def find_chrome() -> str:
    """Find a Chrome/Chromium binary on macOS or Linux."""
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "/Applications/Arc.app/Contents/MacOS/Arc",
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chrome"),
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    raise FileNotFoundError(
        "Chrome/Chromium not found. Install Google Chrome or pass --chrome /path/to/chrome"
    )


def html_escape(text: str) -> str:
    if text is None:
        return ""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def render_headlines(headlines: list) -> str:
    if not headlines:
        return ""
    items_html = ""
    for i, h in enumerate(headlines, 1):
        text = html_escape(h.get("text", ""))
        tag = html_escape(h.get("tag", "")) if h.get("tag") else ""
        tag_html = f'<span class="headline-tag">{tag}</span>' if tag else ""
        items_html += f"""
        <div class="headline-item">
            <div class="headline-num">{i:02d}</div>
            <div class="headline-content">
                {tag_html}
                <div class="headline-text">{text}</div>
            </div>
        </div>
        """
    return f"""
    <section class="section headlines-section">
        <div class="section-eyebrow">The Brief</div>
        <h2 class="section-title-headlines">Headlines</h2>
        <div class="headlines-list">{items_html}</div>
    </section>
    """


def render_item(item: dict) -> str:
    title = html_escape(item.get("title", ""))
    what = html_escape(item.get("what", ""))
    matters = html_escape(item.get("matters", ""))
    your_lens = html_escape(item.get("your_lens", "")) if item.get("your_lens") else ""
    source_url = item.get("source_url", "")
    source_label = html_escape(item.get("source_label", "Source"))
    date = html_escape(item.get("date", ""))

    your_lens_html = ""
    if your_lens:
        your_lens_html = f"""
        <div class="item-callout">
            <div class="callout-label">For You</div>
            <div class="callout-text">{your_lens}</div>
        </div>
        """

    source_html = ""
    if source_url:
        source_html = f"""
        <div class="item-source">
            <a href="{source_url}">{source_label}</a>
            <span class="item-date">{date}</span>
        </div>
        """

    return f"""
    <article class="item">
        <h3 class="item-title">{title}</h3>
        <p class="item-what">{what}</p>
        <p class="item-matters">{matters}</p>
        {your_lens_html}
        {source_html}
    </article>
    """


def render_section(section: dict) -> str:
    items = section.get("items", [])
    if not items:
        return ""
    title = html_escape(section.get("title", ""))
    icon = html_escape(section.get("icon", "")) if section.get("icon") else ""
    items_html = "".join(render_item(item) for item in items)
    icon_html = f'<span class="section-icon">{icon}</span>' if icon else ""
    return f"""
    <section class="section">
        <div class="section-header">
            {icon_html}
            <h2 class="section-title">{title}</h2>
        </div>
        <div class="items">{items_html}</div>
    </section>
    """


def render_html(report: dict) -> str:
    metadata = report.get("metadata", {})
    date = html_escape(metadata.get("date", ""))
    period = html_escape(metadata.get("period", ""))
    topic = metadata.get("topic", "general")
    topic_label = "" if topic == "general" else f" · {html_escape(topic).title()}"

    headlines_html = render_headlines(report.get("headlines", []))
    sections_html = "".join(render_section(s) for s in report.get("sections", []))

    footer = report.get("footer", {})
    user_stack = html_escape(footer.get("user_stack", ""))
    sources_scanned = footer.get("sources_scanned", [])
    sources_html = " · ".join(html_escape(s) for s in sources_scanned)
    generated = datetime.now().strftime("%B %d, %Y · %I:%M %p")

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>AI Radar — {date}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>

@page {{
    size: A4;
    margin: 24mm 22mm 22mm 22mm;
}}

@page :first {{
    margin: 0;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

html, body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #18181b;
    -webkit-font-smoothing: antialiased;
    font-feature-settings: 'ss01', 'cv11';
}}

a {{ color: inherit; text-decoration: none; }}

/* Cover page */
.cover {{
    page-break-after: always;
    height: 297mm;
    width: 210mm;
    padding: 32mm 22mm 22mm 22mm;
    display: flex;
    flex-direction: column;
    background: #ffffff;
    position: relative;
    overflow: hidden;
}}

.cover::before {{
    content: "";
    position: absolute;
    top: 0; right: 0;
    width: 100mm; height: 100mm;
    background: radial-gradient(circle at top right, rgba(99, 102, 241, 0.08), transparent 70%);
    pointer-events: none;
}}

.cover-eyebrow {{
    font-size: 9pt;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: #6366f1;
    margin-bottom: 32mm;
    position: relative;
    z-index: 1;
}}

.cover-title {{
    font-size: 64pt;
    font-weight: 700;
    letter-spacing: -0.035em;
    line-height: 0.95;
    margin-bottom: 16px;
    color: #0a0a0a;
    position: relative;
    z-index: 1;
}}

.cover-subtitle {{
    font-size: 14pt;
    font-weight: 400;
    color: #52525b;
    line-height: 1.5;
    max-width: 460px;
    margin-top: 24px;
    margin-bottom: auto;
    position: relative;
    z-index: 1;
}}

.cover-meta {{
    border-top: 1px solid #e4e4e7;
    padding-top: 20px;
    display: flex;
    justify-content: space-between;
    font-size: 10pt;
    color: #71717a;
    position: relative;
    z-index: 1;
    margin-top: 30mm;
}}

.cover-meta-block {{
    display: flex;
    flex-direction: column;
    gap: 4px;
}}

.cover-meta-label {{
    font-size: 8.5pt;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #a1a1aa;
}}

.cover-meta-value {{
    color: #18181b;
    font-weight: 500;
    font-size: 11pt;
}}

/* Section base */
.section {{
    margin-bottom: 32px;
}}

.section-header {{
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 18px;
    padding-bottom: 10px;
    border-bottom: 1px solid #e4e4e7;
}}

.section-eyebrow {{
    font-size: 8.5pt;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: #6366f1;
    margin-bottom: 8px;
}}

.section-icon {{
    font-size: 14pt;
    color: #6366f1;
    font-weight: 400;
}}

.section-title {{
    font-size: 18pt;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: #0a0a0a;
}}

.section-title-headlines {{
    font-size: 22pt;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: #0a0a0a;
    margin-bottom: 18px;
}}

/* Headlines section */
.headlines-section {{
    background: #fafafa;
    border-radius: 14px;
    padding: 26px 28px 24px;
    margin-bottom: 36px;
    border: 1px solid #f4f4f5;
}}

.headlines-list {{
    display: flex;
    flex-direction: column;
    gap: 14px;
}}

.headline-item {{
    display: flex;
    gap: 18px;
    align-items: flex-start;
}}

.headline-num {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 9pt;
    color: #a1a1aa;
    padding-top: 2px;
    min-width: 24px;
    font-weight: 500;
}}

.headline-content {{ flex: 1; }}

.headline-tag {{
    display: inline-block;
    font-size: 8pt;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6366f1;
    background: rgba(99, 102, 241, 0.08);
    padding: 2px 8px;
    border-radius: 4px;
    margin-bottom: 6px;
}}

.headline-text {{
    font-size: 11.5pt;
    line-height: 1.5;
    color: #18181b;
    font-weight: 450;
}}

/* Items */
.items {{
    display: flex;
    flex-direction: column;
    gap: 22px;
}}

.item {{
    page-break-inside: avoid;
}}

.item-title {{
    font-size: 14pt;
    font-weight: 600;
    color: #0a0a0a;
    letter-spacing: -0.01em;
    margin-bottom: 8px;
}}

.item-what {{
    font-size: 10.5pt;
    color: #27272a;
    margin-bottom: 8px;
    line-height: 1.55;
}}

.item-matters {{
    font-size: 10.5pt;
    color: #52525b;
    margin-bottom: 12px;
    line-height: 1.55;
}}

.item-callout {{
    background: linear-gradient(135deg, #f8f7ff 0%, #f5f3ff 100%);
    border-left: 2px solid #6366f1;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 12px;
}}

.callout-label {{
    font-size: 8pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #6366f1;
    margin-bottom: 4px;
}}

.callout-text {{
    font-size: 10pt;
    color: #312e81;
    line-height: 1.5;
}}

.item-source {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 9pt;
    color: #a1a1aa;
    padding-top: 8px;
}}

.item-source a {{
    color: #6366f1;
    font-weight: 500;
}}

.item-date {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    color: #a1a1aa;
}}

/* Footer */
.report-footer {{
    margin-top: 50px;
    padding-top: 24px;
    border-top: 1px solid #e4e4e7;
    font-size: 8.5pt;
    color: #a1a1aa;
    line-height: 1.6;
}}

.footer-label {{
    font-weight: 500;
    color: #71717a;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 8pt;
    margin-bottom: 4px;
}}

.footer-block {{ margin-bottom: 12px; }}

</style>
</head>
<body>

<div class="cover">
    <div class="cover-eyebrow">AI Radar{topic_label}</div>
    <h1 class="cover-title">What's<br>Actually<br>New.</h1>
    <p class="cover-subtitle">A fast scan of the AI ecosystem, filtered through your stack.<br>Built for shipping, not scrolling.</p>
    <div class="cover-meta">
        <div class="cover-meta-block">
            <span class="cover-meta-label">Report Date</span>
            <span class="cover-meta-value">{date}</span>
        </div>
        <div class="cover-meta-block">
            <span class="cover-meta-label">Period</span>
            <span class="cover-meta-value">{period}</span>
        </div>
        <div class="cover-meta-block">
            <span class="cover-meta-label">Prepared For</span>
            <span class="cover-meta-value">BraindAI</span>
        </div>
    </div>
</div>

{headlines_html}

{sections_html}

<div class="report-footer">
    <div class="footer-block">
        <div class="footer-label">Filtered Through Stack</div>
        <div>{user_stack}</div>
    </div>
    <div class="footer-block">
        <div class="footer-label">Sources Scanned</div>
        <div>{sources_html}</div>
    </div>
    <div class="footer-block">
        <div class="footer-label">Generated</div>
        <div>{generated}</div>
    </div>
</div>

</body>
</html>
"""


def html_to_pdf_chrome(html_path: Path, pdf_path: Path, chrome_bin: str):
    """Use Chrome headless to convert HTML file to PDF."""
    cmd = [
        chrome_bin,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        f"file://{html_path.absolute()}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(f"Chrome failed: {result.stderr}")
    if not pdf_path.exists():
        raise RuntimeError("Chrome ran but no PDF was created")


def main():
    parser = argparse.ArgumentParser(description="Generate AI Radar PDF report")
    parser.add_argument("--input", required=True, help="Path to JSON report file")
    parser.add_argument("--output", required=True, help="Path for output PDF")
    parser.add_argument("--chrome", help="Path to Chrome binary (auto-detected)")
    parser.add_argument("--html-only", action="store_true", help="Output HTML only")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(input_path) as f:
        report = json.load(f)

    html = render_html(report)

    # Always write HTML alongside PDF for inspection
    html_path = output_path.with_suffix(".html")
    html_path.write_text(html)

    if args.html_only:
        print(f"HTML written to: {html_path}")
        return

    chrome_bin = args.chrome or find_chrome()
    html_to_pdf_chrome(html_path, output_path, chrome_bin)
    print(f"PDF generated: {output_path}")
    print(f"HTML preview:   {html_path}")


if __name__ == "__main__":
    main()
