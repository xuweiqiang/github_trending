"""Export GitHub trending 24h ranking to JSON/Markdown."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from github_trending import fetch_trending_star_growth_24h

CST = timezone(timedelta(hours=8))


def _build_markdown(data: dict) -> str:
    now = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S %z")
    lines = [
        "# GitHub 24h Star 增长榜",
        "",
        f"- 生成时间: {now}",
        "",
        "| 排名 | 项目 | 24h 增长 | 总 Stars | 链接 |",
        "|---:|---|---:|---:|---|",
    ]
    for idx, item in enumerate(data.get("items", []), start=1):
        lines.append(
            f"| {idx} | `{item['repo']}` | {item['stars_today']} | "
            f"{item.get('total_stars') or '-'} | [跳转]({item['url']}) |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    data = fetch_trending_star_growth_24h(limit=20)
    data_dir = ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    (data_dir / "trending_24h.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (data_dir / "trending_24h.md").write_text(_build_markdown(data), encoding="utf-8")

    print(f"items: {len(data.get('items', []))}")


if __name__ == "__main__":
    main()
