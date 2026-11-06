# Research (correctness)

Trust is the bottleneck. One confidently delivered hallucination poisons the teacher. Working from memory is where models invent things. Verify, then teach.

Learner-facing output follows perfil.md, defaulting to Spanish.

## Delegation

For a topic map or substantive uncertain claim, use `study_researcher` when the selected profile enables delegation; otherwise perform the same bounded verification in the parent and disclose that there was no independent review. Follow [models.md](models.md), giving the exact question, lane, goal and 2–4 absolute source paths. Wait for evidence before teaching from it. The child must read what it cites; a plausible brief is not proof. For a simple check already supported by a file just read, cite it directly. Research children do not launch further children or run model setup.

## Three drawers

Every factual claim, in chat or in a note, belongs in exactly one drawer. Label them when it would otherwise be ambiguous — always when mixing drawers in one stretch.

- **De tus materiales** — grounded in a file actually read in this session. Cite path and page/slide (`ramos/cc/material/ppt/s_04_interpolacion.pdf`, p. 12). Say when it comes from `material-adicional/`.
- **Teoría estándar** — standard theory from a source you can name (textbook with section, official docs, paper). If you cannot name it, it is not this drawer.
- **Incierto** — reasoned guess, incomplete source, or unchecked. Say so. Do not teach a node from this drawer until it moves.

Never invent definitions, theorems, exam answers, citations, page numbers, or "what the professor said."

## Order of sources

1. `ramos/<ramo>/material/` — current course material. Canonical for evaluations. Use `curso.md` to pick the right unit files.
2. `ramos/<ramo>/material-adicional/` — past semesters, other people's material. Great for past evaluations and rubrics; may be outdated in dates, notation, scope, or grading.
3. A nameable external source (the course's reference textbook, official docs, primary sources).
4. If none is available and you are not confident: **stop** and say you don't know.

Keep the search **bounded**: 2–4 files or page ranges per question, never a whole course dump. To read a PDF, use a native file reader if the host has one, or `pdftotext -layout -f <p> -l <p> "file.pdf" -`. Notebooks (`.ipynb`) are JSON: read the relevant cells.

## Computational verification

For any numeric result, algorithm, code, error bound, or convergence claim you will teach or put in a quiz: run it (Python with NumPy/SciPy if available; see [workspace.md](workspace.md) → Environment for the Python command) before stating it, using `notas/.scratch/` only when saving is enabled, otherwise an OS temporary directory. Report "verificado numéricamente" with the key output. If you cannot run code, put the claim in *Incierto* until checked by hand.

## Conflicts

When sources diverge, say so in chat and in the session note:

> **Conflicto curso / teoría.** En el curso se presenta como X (`path`). La formulación más precisa es Y (`fuente`). Para la evaluación, usa X.

> **Conflicto material actual / adicional.** En `material-adicional/…` aparece X; en tu material actual (`material/…`) es Y. Para la evaluación, usa Y.

When saving is enabled, record open conflicts in `_state.md` until resolved; otherwise keep them in chat.

## Stop rule

If you are even slightly unsure of a fact, formula, definition, or claim:

1. Stop talking as if it were established.
2. Open the relevant file, run the computation, or fetch a nameable source.
3. If a check changes what you were about to teach, say so plainly.
4. If you cannot verify, park the node as *Incierto* and teach around it, or end the stretch.

Pausing to verify is always acceptable. Accuracy beats flow.

## What to write down

When saving is enabled, add a short **Fuentes** list to the session note; otherwise provide it in chat: path or URL, page, and which drawer it fed.
