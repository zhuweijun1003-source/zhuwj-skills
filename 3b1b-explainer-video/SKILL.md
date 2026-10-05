---
name: 3b1b-explainer-video
description: Create high-quality 3Blue1Brown-style Manim animated explainer videos with optional Chinese or multilingual TTS narration for any technical topic. Use when user asks for 3b1b style animation, Manim explainer video, geometric intuition video, mathematical animation of a concept, or to turn an explanation into a polished narrated video. Triggers on 3b1b, 3Blue1Brown style, Manim video, geometric explainer, animated math explanation, 做动画讲解, 3b1b动画.
---

# 3Blue1Brown Style Explainer Video

Produce self-contained Manim Community animated videos that explain technical concepts through geometric intuition, progressive visual build-up, and clean mathematical typography. Optionally add natural TTS narration and mux into a final MP4.

## When to Use

- User requests a 3b1b / 3Blue1Brown style video or animation of a concept
- User wants a geometric / visual / intuitive animated explanation
- User provides a topic (or previous text/HTML explanation) and says “做成动画”, “做成视频”, “加旁白”, “拉长详细版”
- Prefer this over pure image-sequence skills when the content benefits from continuous motion, vector fields, trajectories, equation morphing, or coordinate geometry

## Core Pipeline (follow in order)

1. **Topic → Narrative Script** (must start with a 8–12 s hook)
2. **Script → Scene Design (geometric beats)**
3. **Manim Implementation** (Chinese-capable)
4. **TTS Narration** (via Voice connected tool)
5. **Render + Timing Sync + Mux**
6. **Delivery** (MP4 + source)

Do not skip the geometric design step. 3b1b quality comes from visual metaphors, not from simply animating text.

## 1. Narrative Script

Write a clear spoken script first (Chinese by default if user is Chinese-speaking; otherwise match user language).

### Mandatory Hook (3-Second Attraction Rule)

Every video **must** open with an 8–12 second hook before the formal title or “欢迎来到…”. The first 3 seconds decide whether the viewer stays. Design the hook to create immediate curiosity, surprise, or tension.

Effective hook patterns (pick one or combine lightly):

- **Counter-intuitive claim**: “大模型并不是在‘理解’语言，它只是在高维空间里做加权平均。”
- **Visual paradox / striking image**: a simple object that suddenly transforms into a complex geometric structure.
- **Question that hurts**: “为什么 GPT 能写出从未见过的句子，却还会算错 2+3？”
- **Tiny demo of the core idea**: show the key geometric action in pure form (e.g. one attention arrow pulling a point) before naming anything.
- **Scale shock**: “这个模型的参数数量，比银河系的星星还多。”

Hook rules:
- Spoken length ≈ 8–12 seconds (roughly 40–70 Chinese characters or 25–45 English words).
- Must be visually supported by a fast, clean geometric animation (not just text).
- Immediately after the hook, transition into the formal title + core metaphor statement.
- Never start with “大家好，今天我们来讲…” or any soft welcome.

### Main Script

- Target 2–4 minutes total (including hook) for a focused topic (≈ 450–1000 Chinese characters or 550–1300 English words).
- Structure in progressive sections that map 1:1 to visual scenes.
- Prefer concrete geometric language (“向量场”, “高度图”, “轨迹爬坡”, “梯度方向”) over abstract jargon.
- End with a memorable two-image summary when possible.

Save as `narration_script.txt` in the working artifacts.

## 2. Geometric Scene Design

Before coding, decide the key visual metaphors. Common high-value patterns:

| Concept type          | Preferred visual metaphor                  |
|-----------------------|--------------------------------------------|
| Policy / mapping      | Vector field or arrows on a plane          |
| Value / expected return | Height map / landscape / contour layers  |
| Trajectory / episode  | Path climbing or flowing on the landscape  |
| Recursion / Bellman   | Building blocks that light up in sequence  |
| Comparison            | Side-by-side cards or dual coordinate systems |
| Continuous vs discrete| Grid vs continuous arrows / probability clouds |
| Optimization          | Particles or arrows being gently pushed    |

### Hook Scene (required)

The first scene of the Manim video is the hook. It must:

- Last roughly 8–12 seconds of screen time.
- Open with motion or a surprising transformation within the first 1–2 seconds (the “3-second rule”).
- Visually embody the core insight or paradox of the topic without heavy text.
- End by morphing or cutting cleanly into the formal title card.

Each subsequent section of the script must have at least one strong visual that is not just text. Aim for 6–10 distinct scenes total (hook + 5–9 content scenes) for a 2–3 min video.

## 3. Manim Implementation

### Environment

- Manim Community is available (`manim` command).
- Chinese fonts: use `Noto Sans CJK SC` (already on system). Set `config.font = "Noto Sans CJK SC"`.
- Dark 3b1b palette (recommended tokens):

```python
BLUE = "#58a6ff"
GREEN = "#3fb950"
PURPLE = "#a371f7"
RED = "#f85149"
ORANGE = "#f0883e"
GRAY = "#9a9aa8"
DARK = "#0a0a0c"
```

- Background: `config.background_color = "#0a0a0c"`
- Prefer `MathTex` for equations, `Text(..., font="Noto Sans CJK SC")` for Chinese labels.

### Style Rules

- **Hook first**: the construct() method must start with a dedicated hook scene that delivers motion or a surprising transformation inside the first 1–2 seconds of screen time.
- Progressive disclosure after the hook: introduce one idea at a time, then combine.
- Use `LaggedStart` for groups of arrows / dots.
- Pulse / highlight important objects with brief stroke-width or color changes.
- Keep on-screen text minimal; let the geometry carry the meaning.
- Total silent video length should be close to narration length (or plan to time-stretch later). Prefer writing longer Manim scenes over heavy setpts stretching (>1.4× makes motion look sluggish and exposes layout flaws).

### Layout Safety (critical — prevents text/graphic misalignment)

Root causes of past misalignment:
- Manual `.next_to()` on many objects without consistent buff → overlap or uneven gaps
- Chinese `Text` has different ascent/descent than Latin; centering with `move_to(box)` alone is often vertically off
- Labels placed on dense dots without collision checks
- VGroup.arrange() followed by individual shifts that break relative alignment
- Too-small buff values (<0.15) when Chinese characters are involved

Mandatory layout rules:
1. Prefer `VGroup(...).arrange(DOWN/RIGHT, buff=0.25–0.4)` over chains of `.next_to()` for related items.
2. For text inside a shape: put both in a VGroup and `arrange(ORIGIN)` or use `text.move_to(box.get_center())` then nudge with `.shift(DOWN*0.02)` if needed; never rely on default baseline.
3. Keep a safe margin from frame edges: no object closer than 0.4 units to the border.
4. Labels next to dots/arrows: buff ≥ 0.15; if more than 6 labels, reduce font_size or show only key ones.
5. After building a complex group, call `group.move_to(ORIGIN)` or explicit shift once — avoid scattered absolute coordinates.
6. When mixing MathTex and Chinese Text, place them in separate VGroups; do not assume equal height.

### Motion Density (critical — prevents “too little change”)

Root causes of static-looking scenes:
- Over-use of `FadeIn` + long `wait()` with no further motion
- Objects appear then sit still for 3–5 seconds
- Only one animation type per scene (e.g. only GrowArrow)
- Heavy time-stretching of a short, sparse video

Mandatory motion rules:
1. Every 2.5–3.5 seconds of screen time must contain at least one meaningful visual change (Transform, shift, Indicate, color change, new element, path draw, etc.).
2. Prefer `Transform` / `ReplacementTransform` / `Morph` over pure FadeIn when introducing a related concept.
3. After a group appears, give it a secondary action (pulse, slight drift, highlight sequence) before the next section.
4. Avoid `wait(>2.0)` unless a continuous animation (path, updater) is already running.
5. Target silent-video duration ≥ 75% of narration duration so setpts ratio stays ≤ 1.35.

### Advanced Techniques (richer / more precise graphics)

Pull from `references/advanced-animation.md`. Minimum expectations per major section:

1. **Geometry before algebra** — show the visual mechanism, then the formula.
2. **Opacity hierarchy** — hero 1.0, context 0.35–0.5, axes/grids 0.12–0.2.
3. **ValueTracker + always_redraw** when a parameter drives geometry (angles, positions on curves, progress).
4. **Smart transforms** — `TransformMatchingTex` for equations; `Transform` / `ReplacementTransform` for related shapes; avoid FadeOut+FadeIn of unrelated objects.
5. **Deliberate rate_func** — `smooth` default; `linear` for orbits; `there_and_back` for emphasis; `rush_into` for impact.
6. **Indication** — one `Indicate` / `Circumscribe` / `Flash` on the key object after it appears.
7. **LaggedStart** for groups (arrows, dots, cards) with lag_ratio 0.06–0.12.
8. **Camera zoom** (`MovingCameraScene`) when a dense diagram needs focus, instead of shrinking labels.
9. Vary entrance styles across sections (Create / Write / FadeIn / GrowFromCenter / DrawBorderThenFill).

### Rendering Strategy

- First pass: `-ql` (low quality) to validate timing and layout.
- **Frame QA (required)**: after `-ql`, extract 6–8 frames with ffmpeg (`fps=1/5`), visually check for overlap, cut-off text, and dead static stretches. Fix before `-qm`.
- Final: `-qm` (720p) or `-qh` (1080p) if time allows.
- Always `--disable_caching` during iteration to avoid stale partials.
- Long renders → run in background with `nohup` or `background: true` and poll the log.

Template skeleton lives in `assets/manim_skeleton.py`. Copy and adapt it.

## 4. TTS Narration

Use the connected Voice tool (do not invent local TTS if Voice is available):

```
voice_generate_speech(
  text=<full script>,
  voice="atlas",          # or aurora / helios etc. — pick clear educational voice
  language="zh",          # or "en" / "auto"
  dest_path="narration.mp3",
  with_timestamps=True    # useful for future subtitle work
)
```

List voices first with `voice_list_voices` if the user wants a specific gender/style.

## 5. Sync & Mux

Measure both durations with ffprobe. If they differ, time-stretch the video:

```bash
ffmpeg -y -i video.mp4 -i narration.mp3 \
  -filter_complex "[0:v]setpts=<ratio>*PTS[v]" \
  -map "[v]" -map 1:a \
  -c:v libx264 -preset medium -crf 20 -c:a aac -b:a 192k -shortest \
  final.mp4
```

`ratio = audio_duration / video_duration`. Prefer stretching video rather than speeding audio (keeps speech natural).

## 6. Delivery

Always return:

- Final MP4 (absolute path under `/home/workdir/artifacts/`)
- Source Manim `.py`
- Narration `.mp3` (and timestamps if generated)
- Brief note of duration, resolution, and main visual metaphors used

## Quality Checklist (before delivering)

- [ ] Opens with a clear 8–12 s hook that creates curiosity or surprise in the first 3 seconds
- [ ] Hook is visually driven (motion / transformation), not pure text
- [ ] Every major claim has a corresponding geometric visual
- [ ] Geometry appears before (or with) the equation, not after a wall of text
- [ ] Opacity hierarchy visible (hero bright, context dim, axes faint)
- [ ] At least one smart Transform or ValueTracker-driven motion in the video
- [ ] No overlapping text/shapes; no text cut off at edges (verified via frame QA)
- [ ] Motion density: meaningful visual change at least every ~3 seconds
- [ ] setpts stretch ratio ≤ 1.35 (otherwise add more Manim animation, do not over-stretch)
- [ ] Chinese text renders correctly (no missing glyphs)
- [ ] Color palette is consistent and high-contrast on dark background
- [ ] Narration and visuals roughly aligned
- [ ] File opens and plays with audio
- [ ] Source is clean enough for the user to iterate

## Common Pitfalls

- Starting with a soft welcome (“大家好…”) instead of a hook — violates the 3-second rule.
- **Text/graphic misalignment**: caused by manual next_to chains, insufficient buff for Chinese, or centering Text inside shapes without VGroup.arrange. Fix with arrange() + safe margins.
- **Static scenes**: only FadeIn + long wait. Fix by adding Transform, secondary pulse, or path motion; keep waits ≤ 2 s unless motion is ongoing.
- **Over-stretching**: setpts > 1.5× makes everything sluggish and exposes layout bugs. Write longer scenes instead.
- RoundedRectangle in Manim 0.20+ takes `corner_radius` as first positional or keyword; always use keywords for width/height.
- Long Manim renders exceed tool timeout → always background + poll.
- Do not hard-code English labels when the user is speaking Chinese.
- Avoid pure text slides; if a section has no geometry, redesign it.

## References

- `references/visual-metaphors.md` — expanded catalog of geometric patterns
- `references/manim-chinese.md` — font, Text, and MathTex notes
- `references/layout-and-motion.md` — root causes and fixes for misalignment and static scenes
- `references/advanced-animation.md` — ValueTracker, smart transforms, rate_func, opacity hierarchy, camera, timing tables (from 3b1b + community best practices)
- `assets/manim_skeleton.py` — template with layout-safe patterns and motion-density examples
