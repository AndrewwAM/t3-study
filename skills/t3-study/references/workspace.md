# Study workspace conventions

Apply only inside an explicitly invoked `t3-study` lesson. Every path below is relative to the repository root resolved by the skill, not the current working directory. The user's no-save or task-switch instructions take precedence over persistence defaults.

## Layout

- `ramos/<ramo>/` — one folder per course. `<ramo>` is a short lowercase slug (`cc`, `ia`, `calculo-2`).
  - `curso.md` — course profile: name, code, evaluations and dates, syllabus by unit, file map. Create it with [course setup](course-setup.md).
  - `material/` — the learner's **current** course material (syllabus, slides, guides, rubrics, notebooks). Canonical for evaluations. Read-only.
  - `material-adicional/` — extra material from other people or past semesters (e.g. `material-adicional/2026.1-lucas/`). Good for practice, past exams, and rubrics. Read-only. May be outdated: never let it override `material/`.
- `notas/` — the only place you write study content. Obsidian-compatible vault.
  - `notas/index.md` — list of active topics (create it from `templates/index.md` if missing).
  - `notas/<ramo>/<tema>/_state.md` and `notas/<ramo>/<tema>/sessions/YYYY-MM-DD-slug.md` for course study.
  - `notas/independiente/<tema>/…` for topics not tied to a course.
- `templates/` — copy `state.md`, `session.md`, `curso.md`, `index.md` from here. Do not invent another structure.

## How a session starts

The chat **is** the classroom. After explicitly invoking `t3-study`, the learner names the matter in natural language; you resolve it to a course + scope:

| Learner says | You do |
|---|---|
| `estudiar cc` | Course lane. Read `ramos/cc/curso.md`, then ask for the goal (which evaluation or unit) if it is not clear. |
| `estudiar cc para el C2` / `estudiar cc, interpolación` | Same lane; use `curso.md` to bound the scope to that evaluation's units and their files. |
| `practicar cc C2` | Same lane, practice mode: short probe, then exam-style exercises from `material/` and `material-adicional/` past evaluations, graded against rubrics when available. Still follows the quiz rules. |
| `estudiar simulated annealing` (no course) | Ask: which course, or independent topic. Do not guess. |
| `tema independiente: transformers` | Independent lane → `notas/independiente/transformers/`. |
| `seguir cc` / `continuar` | Resume: read `notas/index.md`, then that topic's `_state.md` and last session. Do not re-probe strands already bracketed. |

If `ramos/<ramo>/curso.md` does not exist, offer to run [course setup](course-setup.md) first. If several files could match a request, list 2–4 candidates and ask. Never ingest a whole course folder.

## Two lanes

- **course** — `material/` is canonical for evaluations. Teach the more precise version when standard theory differs, and flag the difference so the learner knows what to write on the test. When `material-adicional/` differs from `material/`, flag it the same way and use `material/`.
- **independent** — primary or nameable sources only. No "what the professor said."

## Math: Unicode in chat, LaTeX in notes

Use Unicode math in chat by default for compatibility across clients. If the learner's client renders LaTeX, `perfil.md` can set `Fórmulas en el chat: latex`. Otherwise:

- **In chat** (explanations, quizzes, grading), write math with Unicode symbols, never `$`:
  - inline: `Ax = b`, `PA = LU`, `x ∈ ℝⁿ`, `A ∈ ℝᵐˣⁿ`, `Aᵀ`, `A⁻¹`, `‖r‖₂`, `x̂`, `κ(A) = σ₁/σₙ`, `xₖ₊₁ = xₖ − f(xₖ)/f′(xₖ)`, `Σᵢ wᵢ f(xᵢ)`, `∫ₐᵇ f(x) dx`, `ε_mach ≈ 2.2·10⁻¹⁶`, `≤ ≥ ≠ ≈ → ⇒ ⊥ ∂ ∇ √ ∞`.
  - Put a formula on its own line inside a fenced code block when it is long, has fractions or matrices, or needs alignment:
    ```
    Rx = Qᵀb        (Q: m×n ortonormal, R: n×n triangular superior)
    ```
  - Matrices as aligned rows in a code block, or described in words.
  - Code identifiers stay in backticks as usual.
- **In notes** under `notas/` (rendered by Obsidian), use LaTeX: inline `$...$`, display `$$...$$`.
- The same formula can appear twice: Unicode in the chat message, LaTeX in the note.

## Quizzes are chat-only by default

Graded questions are written in the chat and answered by typing (`2`, `1 y 3`, `no sé`). Do not use a clickable selection tool for graded questions unless the learner explicitly asks for clickable options; see [quizzes](quiz.md).

## Environment (Linux, macOS, Windows)

- The workspace may run on any OS. On Windows the shell is usually PowerShell: do not assume `bash`, `ls -la`, `cat <<EOF`, or `/` path quirks. Prefer your host's native file tools; for anything else, a short Python script is the portable choice.
- Python may be `python3`, `python`, or `py`: try them in that order and reuse the one that works.
- To read a PDF, prefer your host's native file reader; otherwise `pdftotext -layout -f <p> -l <p> "file.pdf" -` (Poppler). Quote paths: course files often contain spaces and accents.
- If a tool is missing (Python, NumPy, Poppler), say what is missing and point to the README's install section instead of silently skipping verification.

## Write rules

- Read bounded course sources and the named study topic; existing unrelated notes are not automatically context.
- Write study content **only** under `notas/`. [course setup](course-setup.md) may also write `ramos/<ramo>/curso.md`.
- Never modify, move, or delete anything inside `material/` or `material-adicional/`.
- Per topic: `_state.md` (resume file) and `sessions/YYYY-MM-DD-slug.md` (the lesson). Update `_state.md` at the end of every session and `notas/index.md` when a topic becomes active.
- Default to writing the notes as you teach. Do not wait for "anótalo."
- With saving enabled, scratch work (verification scripts, plots in progress) goes in `notas/.scratch/`. In no-save mode use an OS temporary directory instead. All of `notas/`, `ramos/*` (except the example), and `perfil.md` are git-ignored: they are the learner's, not the framework's.
