# T3 Study workspace

This repository contains a study skill and the learner's materials. Handle ordinary questions, coding, file work, and configuration directly. Being in this repository or using words such as “estudiar”, “entender”, “repasar”, or “continuar” does not automatically start a lesson, require a teaching plan, or create study notes.

## Explicit study entrypoint

Use the study workflow only when the user explicitly invokes `$t3-study` (Codex), `/t3-study` (Claude), or asks to use the `t3-study` skill in another host. Read `skills/t3-study/SKILL.md` then; do not load its lesson modules for unrelated work. Model/course configuration through the skill is maintenance, not a lesson.

Direct answers and follow-ups to an explicitly active lesson continue it. Leaving study mode or switching to another task ends that workflow. A bare “continuar” follows the current task, not an automatic search of old study notes. A direct request to write a particular note authorizes that note without activating a full lesson.

## Files

- `ramos/` contains the learner's course files. Preserve originals in `material/` and `material-adicional/`; course setup can create/update `curso.md` when requested.
- `notas/` contains optional study notes. Do not write there as a side effect of ordinary questions or repository maintenance.
- `perfil.md` and `study-models.json` are optional, local learner configuration. Never invent a name, degree, provider connection, or model choice.
- `.agents/` and `.claude/` contain explicit-only entrypoints. `skills/`, `scripts/`, `templates/`, and tests belong to the framework and may be edited for requested maintenance.
- Learner material, notes, profiles, and machine/provider configuration are git-ignored. Do not force-add them to framework commits.

## Maintenance

Use portable Python for scripts that should run on Linux, macOS, and Windows. Model discovery/validation must not launch subagents or create learner notes. Run `python -m unittest discover -s tests -v` for code changes and `git diff --check` before completing an implementation. Respect the host's tool and delegation rules.
