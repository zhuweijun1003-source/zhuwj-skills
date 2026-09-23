#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把采集到的 GitHub Trending 数据 + Agent 写好的注解，渲染成一份说人话的 HTML 日报。

用法:
    python3 build_report.py \
        --raw trending_raw.json \
        --annotations annotations.json \
        --template assets/report_template.html \
        --out report.html

注解文件 annotations.json 结构（由 Agent 每次运行前填写）:
    {
      "summary": {                       // 可选，纯人话的看点
        "lead": "今天 AI Agent 依然霸榜……",
        "daily": "……",
        "weekly": "……",
        "monthly": "……"
      },
      "repos": {                         // 必填，key 为 "owner/name"
        "anthropics/financial-services": {
          "intro": "一句话，说清楚它是什么、给谁用。",
          "tags": ["AI Agent", "金融"]
        }
      }
    }

build_report.py 只负责排版和数据填充，不负责编内容。仓库里没有注解或
注解缺 intro/tags 时，对应卡片会明确标出「待补注解」，而不是硬编一句。
"""

import argparse
import html
import json
import re
import sys
from datetime import datetime

ORDER = ["daily", "weekly", "monthly"]


def _esc(s):
    return html.escape(str(s if s is not None else ""))


def _fmt(n):
    """12345 -> '12,345'"""
    if n is None:
        return "—"
    return f"{int(n):,}"


def _clean_multi(s):
    return re.sub(r"\s+", " ", s or "").strip()


def build_cards(repos, annotations, period_label):
    cards = []
    for r in repos:
        key = f"{r['owner']}/{r['name']}"
        ann = annotations.get("repos", {}).get(key, {})
        intro = _clean_multi(ann.get("intro", "")) if ann else ""
        tags = ann.get("tags", []) if ann else []
        if not intro:
            intro = "<span class='missing'>（这条还没写人话介绍，待补）</span>"
        if not tags:
            tags = ["待补标签"]

        tags_html = "".join(
            f'<span class="tag">{_esc(t)}</span>' for t in tags[:2]
        )

        stars = _fmt(r.get("period_stars"))
        total = _fmt(r.get("total_stars"))
        forks = _fmt(r.get("forks"))
        lang = _esc(r.get("lang") or "—")

        cards.append(
            f"""
            <li class="card">
              <div class="card-head">
                <a class="repo" href="{_esc(r['url'])}" target="_blank" rel="noopener">
                  {_esc(r['owner'])}<span class="slash">/</span>{_esc(r['name'])}
                </a>
                <span class="lang">{lang}</span>
              </div>
              <p class="intro">{intro}</p>
              <div class="tags">{tags_html}</div>
              <div class="meta">
                <span class="period-up"><svg viewBox="0 0 16 16" class="ic" aria-hidden="true"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"/></svg>{period_label} +{stars}</span>
                <span class="dim"><svg viewBox="0 0 16 16" class="ic" aria-hidden="true"><path d="M8 1.5a.75.75 0 0 1 .75.75V2h4.75a.75.75 0 0 1 .75.75v7a.75.75 0 0 1-.75.75h-1.5v2.25a.75.75 0 0 1-.75.75h-7a.75.75 0 0 1-.75-.75V7H2.75a.75.75 0 0 1-.75-.75v-4A.75.75 0 0 1 2.75 1.5H8Zm.75 1.5H3.5v4h5.25v-4Zm-5.25 7h5.25v2.25h-5.25v-2.25Z"/></svg>{total} 星</span>
                <span class="dim"><svg viewBox="0 0 16 16" class="ic" aria-hidden="true"><path d="M5 3.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm0 4a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm-.75 3.25a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm3.75 1.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm1.5-5.5a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM5 10.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm6.75.25a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm-3-9.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z"/></svg>{forks} 分支</span>
              </div>
            </li>
            """
        )
    return "\n".join(cards)


def build_section(repos, annotations, period_key, label):
    cards = build_cards(repos, annotations, label)
    takeaway = annotations.get("summary", {}).get(period_key, "")
    take_html = f"<p class='takeaway'>{takeaway}</p>" if takeaway else ""
    return f"""
      <section class="sec" id="{period_key}">
        <div class="sec-head">
          <h2>{label}热门 <span class="count">{len(repos)} 个</span></h2>
        </div>
        {take_html}
        <ul class="grid">{cards}</ul>
      </section>
    """


def main():
    ap = argparse.ArgumentParser(description="渲染 GitHub Trending 日报")
    ap.add_argument("--raw", required=True)
    ap.add_argument("--annotations", required=True)
    ap.add_argument("--template", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    raw = json.load(open(args.raw, encoding="utf-8"))
    annotations = json.load(open(args.annotations, encoding="utf-8"))
    template = open(args.template, encoding="utf-8").read()

    periods = raw["periods"]
    sections = []
    for key in ORDER:
        if key not in periods:
            continue
        p = periods[key]
        sections.append(build_section(p["repos"], annotations, key, p["label"]))

    lead = annotations.get("summary", {}).get("lead", "")
    lead_html = f"<p class='lead'>{_clean_multi(lead)}</p>" if lead else ""

    fetched = raw.get("fetched_at", "")
    try:
        report_date = datetime.fromisoformat(fetched).strftime("%Y年%m月%d日")
    except Exception:
        report_date = datetime.now().strftime("%Y年%m月%d日")

    total = sum(len(periods[k]["repos"]) for k in periods if k in periods)

    fills = {
        "{{REPORT_DATE}}": report_date,
        "{{FETCHED_AT}}": _esc(fetched),
        "{{LEAD}}": lead_html,
        "{{SECTIONS}}": "\n".join(sections),
        "{{TOTAL_REPOS}}": str(total),
    }
    out = template
    for k, v in fills.items():
        out = out.replace(k, v)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"已生成 {args.out}（{total} 个仓库）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
