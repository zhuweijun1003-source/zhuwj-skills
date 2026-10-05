# Manim + Chinese Notes

## Font

System provides Noto CJK:

```python
config.font = "Noto Sans CJK SC"
```

Use the same font explicitly on every `Text` if you change the global config later:

```python
Text("状态空间", font="Noto Sans CJK SC", font_size=24, color=GRAY)
```

## Math + Chinese

Keep pure math in `MathTex` / `Tex`. Put Chinese in separate `Text` objects and position them with `.next_to()`.

Avoid embedding Chinese inside MathTex; it frequently fails or looks wrong.

## RoundedRectangle Pitfall (Manim ≥ 0.19)

Constructor signature prioritizes `corner_radius`. Always write:

```python
RoundedRectangle(corner_radius=0.12, width=3.0, height=1.6, color=BLUE, fill_opacity=0.12)
```

Positional width/height after a positional corner_radius will raise “multiple values for argument”.

## Performance

- Prefer `-ql` for the first complete run.
- For final delivery use `-qm` (720p30) or `-qh`.
- Long scenes (>90 s) must be launched in the background; poll the log file.
- `--disable_caching` during development prevents stale partial movies.

## Color Tokens (recommended)

```python
BLUE   = "#58a6ff"
GREEN  = "#3fb950"
PURPLE = "#a371f7"
RED    = "#f85149"
ORANGE = "#f0883e"
GRAY   = "#9a9aa8"
DARK   = "#0a0a0c"
```
