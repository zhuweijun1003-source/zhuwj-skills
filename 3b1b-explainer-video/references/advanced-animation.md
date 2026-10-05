# Advanced 3b1b / Manim Animation Techniques

Synthesized from 3b1b/videos, Manim Community docs, adithya-s-k/manim_skill, and browser-use/video-use patterns. Use these to make graphics richer, more precise, and more interesting.

## 1. Creative Principles (from production pipelines)

- **Geometry before algebra**: show the shape / motion first, equation second. The formula should feel earned.
- **Opacity layering**: primary elements opacity 1.0, contextual 0.35–0.5, structural (axes/grids) 0.12–0.2. Never show everything at full brightness.
- **Breathing room**: after every major reveal, `self.wait(0.8–2.0)`. Viewers need time to absorb.
- **One aha per section**: design each scene around a single visual insight, not a slide of facts.
- **Reuse and transform**: prefer `Transform` / `ReplacementTransform` / `TransformMatchingTex` over FadeOut + FadeIn of unrelated objects.

## 2. ValueTracker + always_redraw (continuous precision)

The signature 3b1b technique for “parameter drives geometry”:

```python
t = ValueTracker(0)

def get_arrow():
    return Arrow(ORIGIN, np.array([np.cos(t.get_value()), np.sin(t.get_value()), 0]) * 2,
                 color=BLUE, buff=0)

arrow = always_redraw(get_arrow)
self.add(arrow)
self.play(t.animate.set_value(TAU), run_time=3, rate_func=linear)
```

Patterns:
- Dot on a curve: `f_always(dot.move_to, lambda: axes.i2gp(t.get_value(), graph))`
- Label that follows: `label.add_updater(lambda m: m.next_to(dot, UP, buff=0.15))`
- Always clear updaters when done: `label.clear_updaters()`

## 3. Smart Transforms

| Goal | Tool |
|------|------|
| Morph shape A → shape B | `Transform(a, b)` or `ReplacementTransform(a, b)` |
| Keep identical TeX parts fixed | `TransformMatchingTex(eq1, eq2)` |
| Match by shape similarity | `TransformMatchingShapes(a, b)` |
| Keep original, spawn copy | `TransformFromCopy(a, b)` |

For equations, isolate substrings:

```python
eq1 = MathTex(r"a^2", r"+", r"b^2", r"=", r"c^2")
eq2 = MathTex(r"a^2", r"=", r"c^2", r"-", r"b^2")
self.play(TransformMatchingTex(eq1, eq2))
```

## 4. Rate Functions (feel, not just motion)

Default `smooth` is fine; use others deliberately:

- `linear` — constant speed (orbits, steady progress)
- `there_and_back` — emphasis pulse / wiggle
- `rush_into` / `rush_from` — anticipation or hard stop
- `running_start` — wind-up then go
- `double_smooth` — extra gentle for aha moments

```python
self.play(mob.animate.shift(UP), rate_func=there_and_back, run_time=0.8)
```

## 5. LaggedStart & Composition

```python
# Staggered entrance (signature 3b1b cloud / arrow field)
self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.08), run_time=2)

# Overlapping sequence
self.play(Succession(Create(a), FadeIn(b), Write(c)))

# Parallel related actions
self.play(Create(circle), Write(label), run_time=1.5)
```

## 6. Indication & Attention

```python
Indicate(mob, color=YELLOW, scale_factor=1.15)   # brief pulse
Circumscribe(mob, color=BLUE, fade_out=True)     # draw circle around
Flash(mob.get_center(), color=GREEN, line_length=0.3)
Wiggle(mob, scale_value=1.1, rotation_angle=0.05*TAU)
```

Use after introducing a critical object, not on every element.

## 7. Camera (MovingCameraScene)

When a diagram is dense, zoom instead of shrinking labels:

```python
class ZoomScene(MovingCameraScene):
    def construct(self):
        # ...
        self.play(self.camera.frame.animate.scale(0.5).move_to(focus_mob), run_time=1.5)
        self.wait(1)
        self.play(self.camera.frame.animate.scale(2).move_to(ORIGIN), run_time=1.2)
```

Save/restore: `self.camera.frame.save_state()` → later `Restore(self.camera.frame)`.

## 8. Opacity & Stroke Hierarchy

```python
axes.set_stroke(opacity=0.25)
grid.set_stroke(opacity=0.12)
primary.set_stroke(width=3).set_fill(opacity=0.9)
secondary.set_fill(opacity=0.35)
```

Structural lines thin and dim; the “hero” object thicker and brighter.

## 9. Timing Table (production defaults)

| Beat | run_time | wait after |
|------|----------|------------|
| Hook opening motion | 0.5–0.8 | 0.3 |
| Title / section header | 1.0–1.5 | 0.8–1.2 |
| Key geometric reveal | 1.5–2.5 | 1.5–2.5 |
| Supporting label | 0.6–0.9 | 0.4–0.6 |
| Transform / morph | 1.2–1.8 | 1.0–1.5 |
| Cleanup FadeOut | 0.4–0.6 | 0.2–0.4 |
| Aha moment | 2.0–2.5 | 2.0–3.0 |

## 10. Anti-patterns to avoid

- `.animate.rotate(...)` for true rotation paths → use `Rotate(mob, angle)` instead
- Animating mobjects never added to the scene
- Writing new text on top of old without `ReplacementTransform` / FadeOut
- Full-brightness axes + full-brightness labels + full-brightness hero (no hierarchy)
- Identical entry animation for every section (vary Create / FadeIn / GrowFromCenter / Write)
- lag_ratio = 0 on large groups (everything pops at once → noisy)

## 11. Minimal rich-pattern checklist (per section)

- [ ] At least one `ValueTracker` or continuous updater if a parameter is being explained
- [ ] At least one smart Transform (not only FadeIn)
- [ ] Opacity hierarchy applied
- [ ] One indication (Indicate / Circumscribe / Flash) on the key object
- [ ] rate_func chosen deliberately for the main motion
- [ ] wait after the aha, not only after the last FadeIn
