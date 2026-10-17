#!/usr/bin/env python3
"""
Shared Claude content generation for the exoplanet digest.

One API call per paper returns:
  - English general-audience summary
  - social-media hook (hook / claim / evidence / question)
  - Turkish title + Turkish summary

Used by fetch_papers.py (daily run) and backfill_ai.py (fill old days).
"""

import json
import os
import re
import time

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5")
MAX_TOKENS = 4000

SECTIONS_EN = ["Why It Matters", "What They Did", "Key Findings", "Looking Forward"]
SECTIONS_TR = ["Neden Önemli", "Ne Yaptılar", "Ana Bulgular", "İleriye Bakış"]

EMPTY_HOOK = {"hook": "", "claim": "", "evidence": "", "question": ""}
UNAVAILABLE_HTML = "<p><em>Summary unavailable.</em></p>"

PROMPT = """You are a science communicator writing for a general audience about exoplanet research.

PAPER TITLE: {title}

ABSTRACT: {abstract}

Produce FOUR parts, each wrapped in the exact XML tags shown below, and nothing outside the tags.

<summary_en>
An extended English summary (250-350 words) using exactly these bold section headers, each on its own line, followed by a paragraph:
**Why It Matters**
**What They Did**
**Key Findings**
**Looking Forward**
Guidelines: write for a curious reader with no astronomy background, use everyday analogies, spell out acronyms, use concrete numbers when the abstract gives them, never invent results that are not in the abstract.
</summary_en>

<hook>
A JSON object (valid JSON, double quotes) with keys:
"hook" (attention-grabbing first line, max 100 chars), "claim" (main finding in plain language, max 200 chars), "evidence" (key supporting detail, max 150 chars), "question" (engaging question for readers, max 100 chars). Exciting but accurate.
</hook>

<title_tr>
The paper title translated into Turkish. Keep object names (e.g. WASP-13b, TOI-700) and instrument/mission names unchanged.
</title_tr>

<summary_tr>
A natural, fluent Turkish translation of the English summary, using exactly these bold section headers each on its own line:
**Neden Önemli**
**Ne Yaptılar**
**Ana Bulgular**
**İleriye Bakış**
Use standard Turkish astronomy terminology (e.g. ötegezegen, ışık eğrisi, tayf, yıldız, atmosfer).
</summary_tr>"""


def make_client(max_retries: int = 5):
    """Return an Anthropic client, or None when no key / package is available."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None
    try:
        import anthropic
    except ImportError:
        return None
    return anthropic.Anthropic(api_key=key, max_retries=max_retries)


def format_summary_html(summary: str) -> str:
    """Markdown-ish summary -> HTML. Any line that is only **Header** becomes <h4>."""
    if not summary:
        return UNAVAILABLE_HTML
    out = []
    for block in re.split(r"\n\s*\n", summary.strip()):
        block = block.strip()
        if not block:
            continue
        # A block may be "**Header**\nparagraph text" - split the header off.
        m = re.match(r"^\*\*([^*\n]+)\*\*\s*\n?(.*)$", block, re.DOTALL)
        if m:
            out.append(f"<h4>{m.group(1).strip()}</h4>")
            rest = m.group(2).strip()
            if rest:
                out.append(f"<p>{rest.replace(chr(10), ' ')}</p>")
        else:
            out.append(f"<p>{block.replace(chr(10), ' ')}</p>")
    return "\n".join(out) if out else UNAVAILABLE_HTML


def _tag(text: str, name: str) -> str:
    m = re.search(rf"<{name}>\s*(.*?)\s*</{name}>", text, re.DOTALL)
    return m.group(1).strip() if m else ""


def _parse_hook(raw: str) -> dict:
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        return dict(EMPTY_HOOK)
    try:
        data = json.loads(m.group())
        return {k: str(data.get(k, "")) for k in EMPTY_HOOK}
    except Exception:
        return dict(EMPTY_HOOK)


def generate_all(client, paper: dict) -> dict:
    """
    Generate summary + hook + Turkish for one paper.
    Returns a dict of fields to merge into the paper; {} if generation failed.
    """
    prompt = PROMPT.format(title=paper.get("title", ""), abstract=paper.get("abstract", ""))
    last_err = None
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )
            text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
            summary = _tag(text, "summary_en")
            summary_tr = _tag(text, "summary_tr")
            if not summary or not summary_tr:
                raise ValueError("response missing summary_en or summary_tr")
            return {
                "summary": summary,
                "summary_html": format_summary_html(summary),
                "tweet_hook": _parse_hook(_tag(text, "hook")),
                "title_tr": _tag(text, "title_tr"),
                "summary_tr": summary_tr,
                "summary_html_tr": format_summary_html(summary_tr),
            }
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(2 * (attempt + 1))
    print(f"    ! generation failed for {paper.get('id')}: {last_err}")
    return {}


def is_complete(paper: dict) -> bool:
    """True when the paper already has English summary, hook and Turkish text."""
    html = (paper.get("summary_html") or "").strip()
    return bool(
        paper.get("summary", "").strip()
        and html and html != UNAVAILABLE_HTML
        and (paper.get("tweet_hook") or {}).get("hook")
        and paper.get("summary_tr", "").strip()
    )
