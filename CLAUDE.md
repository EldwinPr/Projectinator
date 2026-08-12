# CLAUDE.md

Pipeline rules for working in this repo. Read `context/RULES.md` first — it
tells you what to load. This file tells you what to *do*. `RULES.md` is the
entry point (session bootstrap: active issue, tracker, index); this file is
the procedure manual it hands off to — hard gates, forbidden patterns, and
the close checklist below apply regardless of which issue you're on.

## Context — read only when relevant, not up front

- Drafting BPMN, use cases, or the workbook → `context/document-writer-only/*.md`
- Authoring or fixing a `.drawio` file (BPMN, ERD, class, state, component) →
  `context/document-writer-only/bpmn-conventions.md` (or the matching
  `*-conventions.md`) for the rules, plus
  `context/document-writer-only/examples/` for verified worked examples and
  `elements.drawio`, the living shape-style reference palette — check the
  palette before guessing a style string, and re-derive the conventions doc
  from it if they ever disagree.
- Need a second opinion / independent audit → `context/guide/cross-model-review.md`
- Documenting how modules communicate → `context/guide/component-conventions.md`
- A recurring gotcha, or about to add one → `context/gotchas.md` (append only,
  newest entry on top — never edit in the middle)

## Hard gates — never skip these

- No code before `plan.md` exists for the active issue and is user-confirmed.
- No implementation starts before preflight passes: declared dependencies are
  Done in `pm/tracker.yaml`, and no scope overlap with another active issue.
- A `plan.md`'s scope IS whatever its sequence diagram shows — nothing outside
  the diagram is in scope for that issue, and nothing in the diagram gets
  skipped without going back to the user first.
- Every use case has an owning entry in `docs/workbook.xlsx` before it becomes
  a tracked issue — no issue gets created from a bare request that hasn't
  been promoted.
- `docs/requests.md` is append-only capture, never a task queue — don't work
  a request directly; promote it to the workbook first.

## Forbidden patterns

- Don't hand-edit column A on the workbook's Entities sheet — it's a deduped
  list; if it's stale, refresh the source instead of typing into it.
- Don't invent a transition on a state diagram that wasn't stated as a
  business rule during elicitation — if you can't point to why, it doesn't
  go on the diagram.
- Don't reuse a `Kode` across the workbook — check both UC sheets before
  assigning a new one.
- Don't treat a Google Sheets formula as portable to `.xlsx` — `UNIQUE`,
  `ARRAYFORMULA`, `QUERY`, `FLATTEN` don't survive the round trip; see the
  comment on the Entities sheet before assuming it's live.
- Don't hand-derive a `.drawio` style string from memory or general BPMN
  knowledge when `context/document-writer-only/examples/elements.drawio`
  exists — this project's installed shape library has repeatedly diverged
  from spec-plausible attribute names (e.g. gateway type is `gwType=`, not
  `symbol=exclusiveGw`); guessing has produced wrong or blank renders every
  time it was tried instead of checked.
- Don't finish a `.drawio` change without exporting it to PNG and actually
  looking at the render — a diagram that "should" be right per the XML has
  repeatedly turned out to have overlapping shapes, labels sitting on top of
  connectors, or crossing Message Flows once actually rendered.

## Terminology rule

When a diagram/document concept has multiple competing informal definitions
across sources, don't invent our own — adopt the version used by the
practitioner standard closest to our context (e.g. SAP/Signavio's Level
0/1/2+ numbering for process landscapes) and cite it in the relevant
conventions file. Keeps terminology defensible to a client or reviewer
instead of internally consistent but unrecognized outside this repo. This
project also standardizes on **"Level"**, not "Tier" — say Level 1/2/3 in
diagram page names and conversation.

## Close checklist

When an issue closes:

1. Reconcile the sequence diagram against what was actually built (as-built
   pass) — same as-is/to-be discipline the BPMN docs already use.
2. Update `context/index/map.yaml` with the new UC/FEAT -> code entry.
3. Update `context/index/decisions.md` if anything durable/architectural was
   decided along the way that isn't captured elsewhere.
4. `pm/tracker.yaml` -> status Done + one-line summary.
5. `pm/log.md` -> append a dated entry, tagged [STATUS]/[DECISION]/
   [DISCOVERY]/[TODO] as appropriate.
6. `pm/active.json` -> point at the next issue, or clear it.
