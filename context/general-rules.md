# General Rules

Stable, rarely-edited conventions that apply regardless of task type. Lessons-learned get written directly into whichever `context/document-writer-only/*.md` conventions doc they concern (or here, if the lesson is cross-cutting and not about a specific diagram/artifact type) as part of finishing the task that surfaced them — not staged in a separate gotchas file first. A prior version of this project kept a standalone `gotchas.md`; in practice every entry there ended up duplicated into the relevant conventions doc anyway, so the staging step was dropped and the file emptied. Distilled from a prior project's `conventions.md` and `pm-system.md`, keeping only what isn't tied to a specific framework.

**Current scope**: this project is documentation-only right now (Phase 1 — BPMN, ERD, workbook, class/component/state diagrams, elicitation). No stack has been chosen and no code exists yet — `coding-conventions/` and coding-phase guides don't exist yet either; they'll be added when the project actually reaches implementation, not before.

## Naming: domain language

Domain/business terms — model names, field names, UI labels — match whatever language the client and the source documents (elicitation notes, workbook, BPMN diagrams) actually use. Pick one language per project at the start and record it here; don't translate domain terms mid-pipeline — a field named after the client's own term in the BPMN/workbook should keep that exact name in the schema, not get silently translated or normalized.

Structural/technical terms (class names, framework conventions, code-level scaffolding) follow whatever the chosen stack's own convention is — that's `coding-conventions/` territory, not this file.

## Planning gate

A `plan.md` must exist under `pm/issues/{id}-{slug}/` and be reviewed/confirmed by the user before work starts on that issue — a documentation issue (drafting a diagram, filling the workbook) or, once this project reaches implementation, a code change. Don't bypass the plan to make a quick fix — if the fix changes what was planned, update `plan.md` first, then do the work against the updated plan. This keeps `plan.md` the actual source of truth instead of drifting from what was really done.

## Definition of "done"

An issue is not done until all of the following happened, in order:

1. Verification passed — for a documentation issue, that means the diagram/sheet/doc was actually reviewed against its relevant `context/document-writer-only/*.md` convention and (where the convention requires it, e.g. BPMN to-be, state diagrams) confirmed with the client. Once this project has code, this step also covers the stack's test suite and linter/formatter — that part doesn't apply yet.
2. `pm/issues/{id}-{slug}/plan.md` status updated to `done`.
3. `pm/tracker.yaml` row updated to done, with a short summary.
4. The corresponding workbook row (`docs/workbook.xlsx`, "UC BPMN" / "UC Non-BPMN" sheet) marked as implemented, if the issue traces back to a UC.
5. `pm/log.md` gets an appended entry — what was asked, what was done, files touched — not just a status flip. Append-only, don't rewrite past entries.
6. `pm/active.json` moves to the next issue.

Skipping straight to step 6 (moving on without the trail) is what makes old work unreconstructable later — don't do it even under time pressure.

## Terminology rule

When a diagram/document concept has multiple competing informal definitions across sources (e.g. "BPMN Level 0" meaning either a single context diagram or a full landscape depending on source), don't invent our own definition — find the version used by a recognized practitioner standard closest to our context (SAP/Signavio for process architecture, since ERP clients are more likely to have encountered that vocabulary than an academic alternative) and cite it explicitly in the relevant conventions file. This keeps our terminology defensible/citable to a client or reviewer, rather than internally consistent but unrecognizable outside this repo.

## Two kinds of documentation, kept separate

- **Project management** (`pm/`) — what's active, what's done, what's next. Append/status-only; doesn't explain *how* the system works, only *what happened*.
- **Context** (`context/`) — durable knowledge about the system itself: conventions, where things live, why decisions were made. Updated as the system evolves, not tied to any one issue.

When an issue's implementation surfaces a new durable fact (a schema change, a new resource, an RBAC change), update the *context* file as part of closing the issue (e.g. `context/index/map.yaml` gets a new entry) — don't leave it only in the issue's `plan.md`/`pm/log.md`, since those record the one-time event, not the resulting permanent state.
