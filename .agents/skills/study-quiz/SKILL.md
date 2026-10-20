---
name: study-quiz
description: Write, ask, and grade a diagnostic or learning-check quiz in the chat during a study session. Use for any question with a definite correct answer. Preference or goal questions are not quizzes.
---

# Chat quizzes

One question at a time, in the chat. The learner answers by typing. You grade only after they answer.

## Construction (every quiz)

1. Every option is a bare claim — no justification in any option. All reasoning goes in the explanation, revealed after the answer.
2. Write the correct claim first, then mutate it into each distractor with the **same skeleton, length, grain size, and register**. Parallelism falls out by construction. The correct option must not be the longest, the most detailed, or the only one with numbers or technical terms.
3. Each distractor is a real error the learner might make (a known misconception, a sign error, a confused definition), yet unambiguously wrong on the intended reading.
4. No asymmetric bolding or formatting.
5. Always include **0. No sé**. It is a probe signal, not a wrong answer.
6. Multiple-correct questions are allowed; say "(puede haber más de una)" in the stem. They are correct only when the selected set matches exactly.
7. **Shuffle** before showing: the correct option's position must vary across quizzes. Never keep it in the position you wrote it.
8. Read the finished set cold. If you can tell which option is right without knowing the material, regenerate — do not patch.
9. Any number in a stem, option, or explanation must be verified first (compute it with Python when available).

Decide the answer key before showing the question and do not reveal it, hint at it, or let it leak through wording until the learner answers.

**Never write the answer key to any file before the learner answers** — not the session note, not `_state.md`, not `notas/.scratch/`. The host shows file edits in the chat, so a key written to disk is a key shown to the learner. Keep it only in your reasoning; when grading, re-derive and verify it from the question itself.

## Asking

```markdown
**Quiz.** <pregunta>

0. No sé
1. <afirmación>
2. <afirmación>
3. <afirmación>
4. <afirmación>

Responde con el número (o números, p. ej. `1 y 3`).
```

Then **stop your turn and wait**. Silence or an unrelated message is not an answer: if the learner changes topic, mark the quiz *pendiente* in the session note and ask whether to come back to it.

Open-answer questions (derive, compute, write the algorithm or code) are also quizzes: state what a complete answer must contain in your private key, wait, then grade item by item, giving partial credit like a rubric would.

## Grading

```markdown
**Quiz — correcto ✓** / **incorrecto ✗** / **no sé**
Tu respuesta: …
Correcta: …
<explicación: por qué la correcta lo es y qué error codifica cada distractor elegido>
```

Characterize what the answer tells you about their edge: slip, isolated gap, or systematic misconception. Do not treat every miss as a misconception; probe around it.

Write the quiz into the session note **only after grading**: question, options in the order shown, learner's answer, verdict, correct answer, short explanation. If the session stops before an answer, record the question (without key) as *pendiente*.

## Clickable options (only on request)

Use a host selection tool (for example Antigravity's `ask_question`) for graded questions **only** when the learner explicitly asked for clickable options. Then still: shuffle yourself, include "0. No sé" as an option, put no hints in option text, grade only after the selection, and record it in the note exactly as above. Goal and preference questions may use such a tool whenever it helps.
