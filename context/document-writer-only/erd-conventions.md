# ERD Conventions

Entity-relationship diagram conventions, system-level. Drafted during Phase 1, refined as real migrations land. There's no single canonical ERD standard (notation varies Chen vs. Crow's Foot) — no spec to extract from, this file is written directly.

## Notation: Crow's Foot

Use Crow's Foot notation — it's what draw.io's ERD shapes default to, and it reads relationship cardinality directly on the connector without a separate legend. Don't mix in Chen-style diamonds for relationships; keep the whole diagram one notation.

Verified against the installed draw.io Desktop's ER shape library (not from `search_shapes` — see the note in `document-writer-only/bpmn-conventions.md` for why):

| Cardinality | connector attribute |
|---|---|
| Exactly one | `ERone` |
| Mandatory one (one and only one) | `ERmandOne` |
| Zero or one | `ERzeroToOne` |
| Many | `ERmany` |
| One or many | `ERoneToMany` |
| Zero or many | `ERzeroToMany` |

Set as `startArrow=<value>` / `endArrow=<value>` on the connecting edge — one end of the relationship gets the source cardinality, the other end the target cardinality. Entity boxes are `shape=table;childLayout=tableLayout;container=1;` with one row per attribute — draw.io's native ER table shape, not a plain rectangle with a text list.

## Keep the model ORM-shaped

The model should mirror what the ORM can express cleanly — one-to-many, many-to-many, and simple one-to-one relationships — not aspirational modeling that fights the ORM once real code is written. If a relationship needs something an ORM handles awkwardly (a relation with its own attributes, a genuinely polymorphic relation, a self-referencing hierarchy), flag it explicitly on the diagram rather than drawing it as if it were a plain relationship — the awkwardness should be visible at design time, not discovered at migration time.

## Naming stays code-legal

Table names and column names on this diagram follow whatever `coding-conventions/*.md` already commits to for this project (ULID primary keys, no DB-level enums, soft-delete columns, naming case convention, etc.) — this diagram should never show a design that the coding conventions would then forbid once it's turned into a real migration. If the ERD and a coding-conventions file disagree, fix the ERD; the coding conventions are the constraint, not a suggestion to negotiate around at diagram time.

## Lifecycle

- **Drafted early** from the workbook's Entities sheet (`document-writer-only/workbook-conventions.md`) plus whatever use cases are confirmed so far — the ERD doesn't wait for every use case to be locked, it grows alongside them.
- **Refined at issue close time** once real migrations exist for the entities that issue touched — the diagram should converge toward "matches the actual schema," not stay a Phase-1 snapshot forever. Same update trigger as `class-diagram-conventions.md`.
- If the workbook's Entities sheet and the ERD disagree about whether an entity exists, the workbook is the intake list (has this been identified as needed) and the ERD is the design (how it actually relates to everything else) — reconcile rather than letting them drift silently.
