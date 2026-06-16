"""Fetch GitHub trending repositories by 24h star growth."""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from html import unescape

import requests

CST = timezone(timedelta(hours=8))
TRENDING_URL = "https://github.com/trending?since=daily"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 github-trending-bot/1.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def _clean_html_text(raw: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw or "")
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def _parse_repo_item(block: str) -> dict | None:
    repo_match = re.search(
        r"<h2[^>]*>.*?<a[^>]*href=\"/([^\"/]+/[^\"/]+)\"",
        block,
        flags=re.S | re.I,
    )
    if not repo_match:
        return None
    repo = repo_match.group(1).strip()

    stars_today_match = re.search(r"([0-9,]+)\s+stars?\s+today", block, flags=re.I)
    stars_today = int(stars_today_match.group(1).replace(",", "")) if stars_today_match else 0

    total_stars = None
    total_stars_anchor = re.search(
        rf'href="/{re.escape(repo)}/stargazers"[^>]*>(.*?)</a>',
        block,
        flags=re.S | re.I,
    )
    if total_stars_anchor:
        stars_num = re.search(r"[0-9][0-9,]*", _clean_html_text(total_stars_anchor.group(1)))
        if stars_num:
            total_stars = int(stars_num.group(0).replace(",", ""))

    lang_match = re.search(r'itemprop="programmingLanguage">\s*([^<]+)\s*<', block)
    language = lang_match.group(1).strip() if lang_match else ""

    desc_match = re.search(r"<p[^>]*>(.*?)</p>", block, flags=re.S | re.I)
    description = _clean_html_text(desc_match.group(1)) if desc_match else ""

    return {
        "repo": repo,
        "url": f"https://github.com/{repo}",
        "stars_today": stars_today,
        "total_stars": total_stars,
        "language": language,
        "description": description,
    }


def fetch_trending_star_growth_24h(limit: int = 20, timeout: int = 20) -> dict:
    limit = max(1, min(int(limit or 20), 100))
    resp = requests.get(TRENDING_URL, headers=DEFAULT_HEADERS, timeout=timeout)
    resp.raise_for_status()

    blocks = []
    for m in re.finditer(r"(<article[^>]*>)(.*?)(</article>)", resp.text, flags=re.S | re.I):
        if re.search(r"\bBox-row\b", m.group(1)):
            blocks.append(m.group(2))

    items = []
    for block in blocks:
        item = _parse_repo_item(block)
        if item:
            items.append(item)

    items.sort(key=lambda x: x.get("stars_today", 0), reverse=True)
    return {
        "source": "github_trending_daily",
        "window": "24h",
        "generated_at": datetime.now(CST).isoformat(),
        "count": min(limit, len(items)),
        "items": items[:limit],
    }


if __name__ == "__main__":
    data = fetch_trending_star_growth_24h(limit=20)
    for i, item in enumerate(data["items"], start=1):
        print(f"{i:>2}. {item['repo']:<40} +{item['stars_today']}")
