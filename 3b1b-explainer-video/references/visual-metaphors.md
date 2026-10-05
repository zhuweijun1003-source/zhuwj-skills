# Geometric Visual Metaphors for 3b1b-style Explainers

Use these as starting points. Prefer one strong, consistent metaphor per video rather than mixing many weak ones.

## Hook (first 8–12 seconds)

The opening must obey the 3-second attraction rule: motion or a surprising transformation must appear within the first 1–2 seconds of screen time. Good hook visual patterns:

- A single simple object that suddenly explodes into many related objects
- A clean geometric shape that morphs into the core metaphor of the topic
- A tiny working demo of the central mechanism (one attention arrow, one gradient step, one trajectory)
- A scale jump (tiny → enormous) that creates immediate awe or cognitive dissonance

After the hook, cut or morph cleanly into the formal title.

## Core Metaphors

### Vector Field / Force Field
- **When**: policies, gradients, flows, recommendations, forces
- **How**: many short arrows on a plane or manifold; color by magnitude or type
- **Animation**: LaggedStart GrowArrow, then optional collective drift

### Height Map / Landscape
- **When**: value functions, loss surfaces, potential energy, expected return
- **How**: layered semi-transparent ellipses or a simple surface; contour lines; peak labels
- **Animation**: fade layers from outer to inner, then draw a climbing trajectory

### Trajectory / Path
- **When**: episodes, optimization paths, state evolution
- **How**: ParametricFunction or successive dots; dashed then solid
- **Animation**: Create along the path with a moving dot

### Building Blocks / Equation Assembly
- **When**: Bellman, recursive definitions, loss = data + regularizer
- **How**: rounded boxes that appear left-to-right with operators between them
- **Animation**: sequential FadeIn + brief pulse on each box

### Side-by-side Comparison Cards
- **When**: discrete vs continuous, model-free vs model-based, before/after
- **How**: two rounded rectangles with title + bullet list; opposing accent colors
- **Animation**: left then right, or simultaneous with staggered text

### Probability Cloud / Soft Region
- **When**: stochastic policies, uncertainty, soft constraints
- **How**: low-opacity Ellipse or multiple overlapping circles around a mean arrow
- **Animation**: FadeIn after the mean action is shown

### Particle Swarm / Agents
- **When**: population methods, exploration, multiple rollouts
- **How**: many small dots that move according to a simple rule
- **Animation**: Update positions each frame or use successive transforms

## Composition Tips

- Start almost empty; add geometry before labels.
- One accent color per semantic role (BLUE = state/structure, GREEN = reward/value, PURPLE = policy/action, RED = problem/failure).
- Leave breathing room; avoid filling the entire frame.
- End on a clean two-element summary whenever possible.
