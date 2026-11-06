---
name: t3-study
description: "Study university courses or independent topics with diagnosis, quizzes, a plan and optional notes. Only when the user explicitly invokes t3-study; academic questions and opening a course folder do not activate it."
---

# T3 Study

Use this skill only for an explicit request to run it. Quoting its name or asking to edit/debug the framework does not start a lesson. The user's current instructions override workflow defaults, including a request not to save notes.

## Resolve scope before acting

Resolve this file's real path; its third parent is the repository root. Resolve all `ramos/`, `notas/`, `templates/`, `perfil.md` and script paths from that root, even when the thread starts in a nested course directory. Do not assume changing a shell directory reloads T3's workspace or instructions.

If `perfil.md` exists, read its language and learning preferences for the requested lesson. Default to Spanish and address the learner as “tú”; do not invent personal details.

Choose the requested operation:

- **Configure models:** follow [models.md](references/models.md) and stop after configuration. No diagnosis, lesson files, or teaching-plan approval.
- **Configure a course:** follow [course-setup.md](references/course-setup.md). This does not start a lesson or require model onboarding.
- **Start/resume a lesson:** resolve its lane below, check models as described in models.md, then follow [workspace.md](references/workspace.md) and [teach.md](references/teach.md). Load [research.md](references/research.md), [quiz.md](references/quiz.md), and [visualize.md](references/visualize.md) only as needed.

Course study uses `ramos/COURSE/curso.md` and bounded material from that course. If the thread is under `ramos/COURSE/` and no other course was specified, infer that course. Independent study uses named books, external courses, papers, links or supplied files without assuming a university course. Ask when the lane or objective is genuinely ambiguous. Never ingest a whole course or vault just to find context.

## Session boundaries and persistence

An explicitly started lesson uses diagnosis → approved plan → teaching, or resumes from its existing state. Answers and direct follow-ups continue that lesson without repeating the invocation. On an unrelated task or “salir del modo estudio”, stop the workflow. Do not turn a bare “continuar” in another task into a saved-lesson search. There is no background transcript recorder.

By default, save actual learning progress under `notas/`, using `templates/`. Course topics use `notas/COURSE/TOPIC/`; independent topics use `notas/independiente/TOPIC/`. Do not fabricate understanding, assessment results, or an approved plan.

**No-save mode:** if the learner asks “sin guardar apuntes” or “solo en chat”, do not create/update notes, index, state, or persistent figures. Keep the plan and progress in the conversation; use an OS temporary directory for necessary computations/figures. Reading an explicitly requested prior topic is allowed, but do not update it. Do not save a new model profile either unless the user separately chooses to save configuration; they may use a selected target for this session or work in the parent. Explain that durable resume will depend on the existing conversation.

Quizzes are answered in chat, and keys are not written to files before the learner answers. Use Unicode math in chat by default and LaTeX in saved notes; a learner preference can override chat formatting. Use the host's actual display capabilities for figures.

## Model/provider portability

The teacher keeps its selected thread model. Study roles use the workspace/environment profile and T3's available delegation tools, as described in models.md; no personal provider ids or preferred model names ship with the repository. Missing T3 discovery tools mean setup is unavailable, not permission to invent models. Continue in the parent when the learner chooses that fallback. Role children execute their bounded assignment; they do not onboard models, start lessons, or recursively delegate.
