---
name: study-course-setup
description: Add or update a course in ramos/ - create the folder layout and write ramos/<ramo>/curso.md (evaluations, dates, units, file map) from the syllabus. Use for "nuevo ramo X", "configurar ramo X", or when a study request names a course without curso.md.
---

# Course setup

This is maintenance work: no probes, no teaching plan.

1. **Slug.** Short lowercase name (`cc`, `ia`, `calculo-2`). Ask if ambiguous.
2. **Folders.** Ensure `ramos/<ramo>/material/` and `ramos/<ramo>/material-adicional/` exist. If they are empty, tell the learner where to put files and stop:
   - current semester files → `material/` (syllabus first);
   - files from someone else or past semesters → `material-adicional/<semestre>-<origen>/` (e.g. `2026.1-lucas/`).
3. **Read the syllabus** (programa, syllabus, planificación) from `material/`. If there is none, ask for it; fall back to `material-adicional/` only with a clear warning that dates and scope may be outdated.
4. **Inventory**, without reading everything: list the folders and file names; open only what is needed to map files to units (first page of slide decks, titles of guides).
5. **Write `ramos/<ramo>/curso.md`** from `templates/curso.md`:
   - name, code, semester, professor, reference textbook;
   - evaluations with date and units covered (state whether cumulative);
   - units in order with their main files in `material/`, and relevant files in `material-adicional/` (past exams, rubrics, guides) marked as such;
   - known differences between current and additional material (different semester, changed order, topics no longer covered).
   Cite the syllabus page for dates and evaluation scopes. Mark anything you inferred rather than read as *(inferido)*.
6. **Show a summary** in chat (evaluations + units) and ask the learner to correct anything wrong. Apply corrections to `curso.md`.

Never modify files inside `material/` or `material-adicional/`. Re-run this skill when the learner adds new material or the syllabus changes; update `curso.md` in place and keep their corrections.
