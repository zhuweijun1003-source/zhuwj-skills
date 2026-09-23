#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抓取 GitHub Trending 的日 / 周 / 月数据，解析为结构化 JSON。

用法:
    python3 fetch_trending.py [--out OUTPUT.json] [--periods daily,weekly,monthly]

输出:
    一个 JSON 对象，结构如下（供后续生成日报使用）:

    {
      "fetched_at": "2026-09-23T14:05:00+00:00",
      "periods": {
        "daily": {
          "range": "today",
          "label": "今日",
          "repos": [
            {
              "owner": "anthropics",
              "name": "financial-services",
              "url": "https://github.com/anthropics/financial-services",
              "lang": "Python",
              "total_stars": 36499,
              "period_stars": 438,
              "forks": 5333,
              "description": "……"
            }
          ]
        },
        "weekly": { ... },
        "monthly": { ... }
      }
    }

失败时非零退出并打印错误信息。该脚本只负责确定性抓取与解析，
不做任何「写介绍 / 打标签」的主观加工——那一步交给 Agent 在注解里做。
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone, timedelta

import requests
from bs4 import BeautifulSoup

# GitHub 反爬较弱但偶发限流，用一个常见 UA 并做有限重试。
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

BASE = "https://github.com/trending"

# period 参数 -> (URL 的 since 值, 页面上「stars 今/本周/本月」文案, 中文明示)
PERIODS = {
    "daily": ("", "stars today", "今日"),
    "weekly": ("weekly", "stars this week", "本周"),
    "monthly": ("monthly", "stars this month", "本月"),
}


def fetch(url, retries=3, backoff=2.0):
    last = None
    for i in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            if resp.status_code == 200:
                return resp.text
            last = f"HTTP {resp.status_code}"
        except Exception as exc:  # noqa: BLE001
            last = str(exc)
        time.sleep(backoff * (i + 1))
    raise RuntimeError(f"抓取失败 {url}: {last}")


def parse_period(html, period):
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.select("article.Box-row")
    repos = []
    for art in articles:
        a = art.select_one("h2 a")
        if not a:
            continue
        href = a.get("href") or ""
        parts = [p for p in href.strip("/").split("/") if p]
        if len(parts) < 2:
            continue
        owner, name = parts[0], parts[1]

        desc_el = art.select_one("p")
        desc = _clean(desc_el.get_text()) if desc_el else None

        lang_el = art.select_one('[itemprop="programmingLanguage"]')
        lang = _clean(lang_el.get_text()) if lang_el else None

        total_stars = _num_from(art.select_one('a[href*="/stargazers"]'))
        forks = _num_from(art.select_one('a[href*="/forks"]'))

        period_stars = None
        m = re.search(r"([\d,]+)\s+" + re.escape(PERIODS[period][1]), art.get_text())
        if m:
            period_stars = _to_int(m.group(1))

        repos.append(
            {
                "owner": owner,
                "name": name,
                "url": BASE + href,
                "lang": lang,
                "total_stars": total_stars,
                "period_stars": period_stars,
                "forks": forks,
                "description": desc,
            }
        )
    return repos


def _clean(s):
    return re.sub(r"\s+", " ", s or "").strip()


def _num_from(el):
    return _to_int(_clean(el.get_text())) if el else None


def _to_int(s):
    try:
        return int(re.sub(r"[^\d]", "", s or ""))
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(description="抓取 GitHub Trending 数据")
    ap.add_argument("--out", default="trending_raw.json")
    ap.add_argument("--periods", default="daily,weekly,monthly")
    args = ap.parse_args()

    wanted = [p.strip() for p in args.periods.split(",") if p.strip() in PERIODS]
    if not wanted:
        print("没有有效的 period，可选：daily,weekly,monthly", file=sys.stderr)
        return 1

    periods = {}
    for p in wanted:
        since, label_txt, label_cn = PERIODS[p]
        url = BASE if not since else f"{BASE}?since={since}"
        print(f"抓取 {label_cn}({p}) …")
        html = fetch(url)
        periods[p] = {
            "range": label_txt,
            "label": label_cn,
            "repos": parse_period(html, p),
        }
        print(f"  -> {len(periods[p]['repos'])} 个仓库")

    payload = {
        "fetched_at": datetime.now(timezone.utc)
        .astimezone(timezone(timedelta(hours=8)))
        .isoformat(timespec="seconds"),
        "periods": periods,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"已写入 {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
