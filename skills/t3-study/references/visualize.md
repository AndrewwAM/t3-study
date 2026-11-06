# Lesson visuals

This is an internal active-lesson module. In no-save mode, use an OS temporary directory for scripts/figures, display the result in chat using host-supported tools, and do not create a viz/ folder or modify notes.

Use a picture for dependencies, flows, sequences, function behavior, convergence, or spatial structure. Skip decoration and pictures that merely repeat a sentence. One idea per picture, fewest carrying elements.

## Structure → Mermaid

Write a Mermaid block directly in the chat and the session note. Obsidian renders it.

```mermaid
graph TD
  A[verdad incondicional] --> B[nodo derivado]
  B --> G[objetivo]
```

Before using it, re-read every arrow: direction means "is needed for". Keep labels short; quote labels with symbols (`A["x = g(x)"]`).

## Plots and geometry → Python

For function plots, errors vs. iterations, interpolation vs. data, vector geometry, and the like:

1. Write a small matplotlib script in `notas/.scratch/` and save a PNG into the topic's `viz/` folder (`notas/<ramo>/<tema>/viz/<nombre>.png`). Use labeled axes, a legend when there is more than one series, log scale where errors span orders of magnitude.
2. **Look at the PNG** with your image/file viewer before using it. Check axes, labels, clipping, and that it shows what you claim.
3. Embed it in the session note with a relative link: `![descripción](../viz/<nombre>.png)`. In chat, show it if the host can display local images; otherwise describe what it shows and point to the file.

If you cannot view images, say the picture was not visually checked. If no correct picture can be made, omit it and say why. Never use an image-generation model for diagrams: arrows and coordinates must be exact.

## Delegation

Use the configured `study_mermaid_maker` role for structural diagrams and `study_visual_maker` for plots, SVG or geometry when delegation is enabled; see [models.md](models.md). Give one concrete brief, source context, target path, and saving mode. A child must inspect any generated PNG before returning and must not delegate again. For small pictures or parent-only roles, do the work yourself. Follow the host's visual display rules; a file created on disk is not necessarily visible in chat.
