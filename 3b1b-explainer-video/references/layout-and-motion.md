# Layout Safety & Motion Density

## Why text and graphics misalign

1. Chains of `.next_to(obj, UP, buff=0.1)` on Chinese labels → uneven gaps and overlaps.
2. `Text.move_to(box)` ignores Chinese baseline; text sits too high or too low inside shapes.
3. Dense dot clouds with individual labels → collisions.
4. Mixing absolute coordinates with later `shift()` breaks earlier relative alignment.
5. `setpts` stretch > 1.4× slows everything and makes small layout errors obvious.

## Fixes (always apply)

- Group related items with `VGroup(...).arrange(DOWN/RIGHT, buff=0.25–0.4)` then one `move_to()`.
- Card pattern: `VGroup(box, VGroup(title, subtitle).arrange(DOWN, buff=0.18))`.
- Edge margin ≥ 0.4 units (`to_edge(..., buff=0.5)` or manual check).
- Label buff next to dots ≥ 0.15; hide secondary labels if > 6 items.
- Prefer fewer, larger labels over many tiny ones.

## Why scenes feel static

1. `FadeIn` everything → long `wait(3)`.
2. Only one animation flavor per section.
3. No secondary action after objects appear.
4. Silent video much shorter than narration → heavy stretch.

## Fixes (always apply)

- At least one meaningful change every 2.5–3.5 s (Transform, Indicate, shift, path, color pulse).
- After a group appears, give a short secondary action (pulse stroke, color flash, slight drift).
- Keep individual `wait()` ≤ 2.0 unless a continuous animation is running.
- Aim for silent video duration ≥ 75 % of narration so stretch ratio ≤ 1.35.
- Prefer `Transform` / `ReplacementTransform` when introducing a related idea.

## Frame QA (required after first -ql render)

```bash
ffmpeg -y -i media/.../Scene.mp4 -vf "fps=1/5" -frames:v 8 /tmp/qa/f%02d.png
```

Visually check each frame for:
- Overlapping text/shapes
- Text cut off at edges
- Large empty regions with no motion for > 3 s of original time

Fix code before the final `-qm` render.
