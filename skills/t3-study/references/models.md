# Configure study roles in T3

The teacher owns setup; role children never configure models or recursively delegate. A configuration request does not start a lesson, ask learner probes, or create notes.

## Profile and scope

Read `study-models.json` at the resolved repository root. It is git-ignored learner configuration, with `schema_version: 1` and an `environments` map keyed by T3's stable `environmentId`. The same workspace profile works with a Codex, Claude or other supported teacher. Do not change the teacher's model, global defaults, provider connections, or authentication as part of study setup.

Three roles are available:

- `study_researcher`: verify a bounded claim or topic map against read sources; return evidence, citations, conflicts and gaps; do not edit files.
- `study_mermaid_maker`: produce a small dependency/structure diagram and verify its arrows, labels and readability.
- `study_visual_maker`: produce a checked plot or geometric figure with code/SVG, rendering and inspecting any PNG before returning.

Each role is a T3 target `{providerInstanceId, model, options}`, or `{"mode":"parent"}` to use the teacher without a child. Include `options` even when empty; do not implicitly inherit unrelated teacher settings.

T3 applies nonempty options as overrides of inherited values; an empty object clears inherited options. When choosing effort while retaining other settings, explicitly set the other applicable options using catalog defaults or the user's choices. Do not silently inherit a premium/fast mode from the teacher. The helper validates the values supplied; it does not invent or expand missing defaults.

## First use or reconfiguration

1. Discover the host's T3 tools. Obtain this machine's identity with `t3_environment_read` and its model catalog with `orchestrator_capabilities`. Use the actual `environmentId`, not a label or hostname. If a catalog already exists in this thread, reuse it. Follow T3's refresh rule: call once before the first delegate and again only after an error or a user-named provider change.
2. Read the profile for this workspace/machine. If absent, **ask before saving or delegating**: offer one balanced assignment, customization, or no subagents. Present provider, model and reasoning options for all three roles with a brief rationale. An explicit user instruction naming their desired models is already a choice; validate it rather than asking again. Wait for a real answer; silence is not acceptance.
3. Recommend only providers with `canRunChildTask=true`, compatible runtime modes and cross-provider support when needed. Choose actual catalog model ids and exact option ids/values. Favor careful evidence checking for research, precise reasoning for plots/geometry, and a lighter suitable choice for small Mermaid diagrams. Existing preferences can guide the proposal when still available. These are heuristics, not benchmark or price guarantees; if you cannot rank candidates confidently, say so. Do not invent model names, price claims or connection status. Exclude disabled providers even if they list models.
4. Validate complete existing profiles and reuse them without repeating setup. If a target becomes unusable, report the affected role and ask about a replacement or parent-only work. Never silently switch provider/model. Choosing parent-only for this session need not persist a preference; ask to save only when the learner wants a durable profile. In a no-save lesson, keep selected targets in conversation unless the user separately authorizes saving configuration.
5. Model catalogs may be truncated (`omittedModels`). A missing model is unverified, not necessarily unavailable. After a validation error for an omitted model, search T3's catalog for it and merge the returned metadata into the current snapshot before checking again. Preserve current provider enablement and constraints.

List availability does not verify authentication, remaining quota or the success of a future launch. Do not launch test subagents during onboarding. If T3 tools are unavailable, explain that catalog-based setup cannot run and offer a parent-only lesson; do not invent an environment id or save that fallback permanently without being asked. If Python is missing, the teacher can validate the same JSON structure against the catalog directly; do not claim the helper passed.

## Portable helper and manual editing

Use `scripts/study_models.py` with the Python launcher available on the machine (`python3`, `python`, or `py`). It uses only the standard library and does not start models, services or study sessions. Run it by absolute path from a course subdirectory, and pass the resolved repository root as `--workspace`.

Save the actual capabilities payload to a temporary JSON file outside the repository, then:

```text
python scripts/study_models.py --workspace . check --environment ENVIRONMENT_ID --catalog /path/to/capabilities.json
```

`setup_required` means there is no saved profile. `needs_attention` means the profile cannot be used as-is. Both return exit status 2 and no executable targets. A valid result returns `ready` and the exact `targets` to use.

The user may edit `study-models.json` manually. Its shape is:

```json
{
  "schema_version": 1,
  "environments": {
    "ENVIRONMENT_ID_FROM_T3": {
      "label": "My computer",
      "roles": {
        "study_researcher": {
          "providerInstanceId": "PROVIDER_ID_FROM_CATALOG",
          "model": "MODEL_ID_FROM_CATALOG",
          "options": {}
        },
        "study_mermaid_maker": {"mode": "parent"},
        "study_visual_maker": {"mode": "parent"}
      }
    }
  }
}
```

For assisted setup, put only the selected environment's `{label, roles}` object in a temporary profile file, and use:

```text
python scripts/study_models.py --workspace . set --environment ENVIRONMENT_ID --catalog /path/to/capabilities.json --profile /path/to/profile.json
python scripts/study_models.py --workspace . show
```

The helper validates enabled providers, cross-provider/runtime compatibility, model ids and exact option values before writing. It preserves other environment profiles and reports malformed config instead of replacing it. Keep credentials out of this file. Back it up with the learner's files and avoid simultaneous edits when syncing between machines.

## Delegation

Use the validated role target as `delegate_task.target`, with settings in `target.options`. T3's delegation tool handles these explicitly selected settings and cross-provider children; do not substitute a native agent with a different model. A parent-only role never launches a child.

Send only the bounded brief, absolute repository/source/output paths, relevant reference (`research.md` or `visualize.md`), role requirements above and saving mode. Include the learner's requested language. Research children return evidence without writes; visual children respect temporary output in no-save mode. Never pass a whole course or conversation merely because it is available.

Wait for relevant evidence before teaching. Follow the returned `next` instruction and the host's completion mechanism instead of polling a running delegate. If a chosen run is replaced or no longer needed, cancel it through T3 before launching a replacement. Do not infer successful independent verification from merely creating a child.
