---
name: github-trending-daily
description: 生成 GitHub Trending 的 HTML 订阅日报。当用户要求「GitHub 热门/趋势日报」「今日/本周/本月 GitHub 热门仓库」、或需要一份汇总 GitHub 热门仓库及其星数、功能简介、技术标签的 HTML 报告时使用。采集 GitHub Trending 官方页（日/周/月）数据，输出说人话、无 AI 腔的排版日报。
---

# GitHub Trending 订阅日报

采集 GitHub Trending（日 / 周 / 月）官方页数据，汇总热门仓库与星数，为每个仓库写一句话「它是干什么的、给谁用」，打 2 个技术标签，渲染成一份说人话的 HTML 日报。

## 工作流程

1. **采集数据**：运行 `scripts/fetch_trending.py` 抓取三个周期，产出 `trending_raw.json`。
2. **写注解**：手动填写 `annotations.json`（人话介绍 + 标签 + 看点），这是唯一需要判断力的步骤。
3. **渲染日报**：运行 `scripts/build_report.py` 合并数据与注解，输出成品 HTML。
4. **自检交付**：用 `html` skill 的 `shot.py` 渲染截图核对排版，再用 `present_files` 交付 HTML。

## 第 1 步：采集

```bash
python3 scripts/fetch_trending.py --out trending_raw.json --periods daily,weekly,monthly
```

- 只做确定性抓取与解析，**不做任何主观加工**。输出结构见脚本 docstring。
- 网络偶发失败会自动重试；连续失败会报错退出，重跑即可。
- 仓库描述为空（如 `anthropics/financial-services`）是正常的，解析为 `null`。

## 第 2 步：写注解（核心，做这一步才算干活）

打开 `trending_raw.json`，对照每个 `owner/name`，在 `annotations.json` 里填：

```json
{
  "summary": {
    "lead": "顶部导读，一句总览……",
    "daily": "今日看点……",
    "weekly": "本周看点……",
    "monthly": "本月看点……"
  },
  "repos": {
    "anthropics/financial-services": {
      "intro": "一句话，说清它是什么、给谁用、用在什么场景。",
      "tags": ["AI Agent", "金融"]
    }
  }
}
```

**写人话的硬要求（避免 AI 腔）：**
- `intro` 只写一句话，句式「它是什么 + 给谁 / 在什么场景用」。要具体，不喊口号。
- **禁用**这类词：赋能、助力、一站式、生态、闭环、解决方案、助力企业、降本增效、开启新时代。
- **禁用**「它是一款……」的模板腔，也禁用感叹号和营销话术。
- 描述为空或拿不准的仓库，先读仓库主页核实再写；实在不知道就写「（待核实）」，绝不硬编。
- `tags` **必须恰好 2 个**，要具体（如 `RAG`、`模型推理`、`浏览器自动化`），不要用「工具」「应用」这种空泛词。
- 仓库在多个周期重复出现时，注解只写一份，按 `owner/name` 复用。

`summary` 可选；不填则日报没有导读，不报错。

## 第 3 步：渲染

```bash
python3 scripts/build_report.py \
  --raw trending_raw.json \
  --annotations annotations.json \
  --template assets/report_template.html \
  --out 日报输出路径.html
```

- 输出是**自包含单文件 HTML**（内联 CSS、内联 SVG 图标、无外部依赖），直接浏览器打开即可。
- 缺注解的仓库卡片会标「待补注解」，不会硬编内容。

## 第 4 步：自检与交付

1. 用 `html` skill 的 `shot.py` 渲染桌面 + 移动截图，核对排版与数据（星数、标签、简介是否都正常显示）。
2. 抽查 2-3 条星数与仓库主页是否一致，防止抓取或注解错位。
3. 用 `present_files` 交付生成的 `.html`，交付说明里写明数据抓取时间与数据源。
