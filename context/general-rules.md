# General Rules

These rules apply across implementation, documentation, and operations work.

**This file is the single owner of the shared working rules** — sources of
truth, work classification, the planning gate, working discipline, and the
definition of done, version control. The runtime manuals (`CLAUDE.md`, and
`AGENTS.md`, generated from it) point here in one line instead of restating any
of it; the only rules they keep in full are the ones whose violation destroys
work, which must be impossible to miss even for a session that never follows a
pointer.

That split is a decision about **what must be impossible to miss**, not
deduplication. The manuals are loaded into every session unconditionally;
`context/` files are read because `RULES.md` says so. Moving a rule out of a
manual changes it from *guaranteed* to *conventional* — so a rule whose
violation destroys data stays there in full, and if a rule moved here later
shows signs of being missed, move it back deliberately rather than restating it
in both places.

**Change a rule here, not there.**

## Current Scope

This is an implementation project with a documentation layer attached. Code is
the deliverable; `docs/` and the diagrams exist to keep it traceable to
something a stakeholder actually said, and to settle questions faster than
prose can.

**Only the ERD is an expected, maintained artifact.** BPMN, class, state and
component diagrams are optional — drawn when they are the fastest way to resolve
or communicate something, skipped when they are not. No code waits on a diagram.

Code, tests and the current schema describe **implemented** behaviour. Confirmed
requirements and specifications describe **intended** behaviour. Surface
conflicts between them rather than silently rewriting one to match the other.

## Sources Of Truth

- **`context/`** records durable facts and working rules — what is *true*.
- **`pm/`** records work state and history — what *happened*. `tracker.yaml` for
  open work, `archive.yaml` for closed, `issues/{slug}/` for the capsule of
  anything open, `log.md` for narrative, `todo.md` for unconfirmed ideas.
- **`docs/`** records requirements, specifications, and client deliverables.
- **`input/`** records raw client source material and is append-only.
- Historical plans explain past decisions but do not override current code,
  schema, or confirmed specifications.
- **`context/shape/`** records business intent per area — what things mean,
  why, which way to lean — verified by the user's quoted word rather than by
  the code. It biases a reading; it never overrides code, and a conflict
  between the two is raised with the user. Its rules are in
  `context/shape/README.md`.

**Every durable rule has exactly one owner in `context/`.** Do not restate one
in an issue file or a second conventions file — update its owner instead. When
work establishes a durable fact, update whichever file owns it:
`context/coder-only/*.md`, `context/document-writer-only/*.md`,
`context/index/map.md`, or `context/index/decisions/`.

An observation that does not yet have an owner is a different thing. It belongs
in `context/gotchas.md`, the buffer the distill pass promotes into `context/`
and then empties (`context/distill.md`). That file is intake, not truth: it is
not read at session start, and it is never deleted.

## Domain Language

Domain and business terms — entity names, field names, UI labels — follow the
language the client and the source documents actually use. Pick one language per
project at the start and record it here. **Do not silently translate or
normalise a load-bearing term**: a field named after the client's own word in
the elicitation notes carries that exact word into the schema.

Structural and technical naming follows the chosen stack's own conventions —
`context/coder-only/` territory, not this file.

When a business term and its technical name diverge, that pair goes in
`context/index/vocabulary.md`. The first time somebody has to ask what a word
maps to is the signal it belongs there.

## Work Classification

- **Implementation.** Features, bugs, regressions, refactors, security fixes,
  upgrades, performance work, data repairs. Enters `pm/tracker.yaml` directly.
- **Business change.** A new capability or a changed business rule is confirmed
  with the user first, then enters the tracker the same way. Raw entries in
  `docs/requests.md`, `input/`, and `pm/todo.md` are unconfirmed source
  material, not specifications.
- **Artifact work.** A diagram, a workbook change, a requirements document —
  requested in its own right, or drawn because it is the cheapest way to settle
  a question. Load `context/document-writer-only/` only then.
- **Questions, investigations and reviews create nothing.** Answer the question.

**No artifact is a prerequisite for code.** A use case does not need a workbook
row, and a change does not need a diagram, before it can be built. Where a
workbook row or an ERD entity already exists for the behaviour, keep it current
as part of the work — that is upkeep, not a gate.

### The external tracker, if the project uses one

`pm/` is the source of truth for issue **state**. An external tracker, if one is
used, is its shared mirror — and the source of issue **identity**. Name it once,
here, and keep the two from drifting.

**An issue's id is the external tracker's identifier, and nothing else.** Create
the external issue first; the id it returns is the id in the `pm/tracker.yaml`
row, the capsule directory (`pm/issues/{id}-short-name/`), the commit message
(`Refs {id}`), and every reference in prose. Search the tracker before creating:
most work already has an issue.

This replaced a scheme worth not re-inventing. `pm/` once minted a per-type code
(`FEAT-12`, `FIX-7`, `TASK-3`…) and the external tracker assigned its own
number, mirrored in an `external:` field. The code failed at its only job, being
a stable handle: four codes were reused for two different issues each, one code
named issues in two different applications, a duplicate existed only because the
code rather than the identifier was being matched on, and the prefix was a
second, weaker copy of `type` that went stale when a "feature" turned out to be
a fix. The external tracker cannot reissue a number. **The cost is accepted**:
an issue cannot be created offline, and a `status: open` row cannot exist before
its external issue does, because before that it has no name.

- **Labels and project are mandatory, and derived rather than chosen** — from
  the row's `type`, its `epic`, and its application if there is more than one.
  Put the mapping table here when the tracker is adopted. Create a new label or
  project only when the user asks; if nothing fits, say so rather than inventing
  a bucket. (Left optional, they lapsed: most open issues ended up with neither.)
- Record the issue URL at the top of the capsule's `plan.md` (`url:`). The id is
  already `id:`; do not write it twice.
- **The external description stands on its own**: the problem, what changed,
  how it was verified, what is left, and any constraint a reader must not
  violate. Point at the `plan.md` path rather than duplicating the spec. For a
  `status: open` row with no capsule, the description is the only detail there
  is.
- Keep it current: when the row's status or summary changes, update the external
  issue in the same pass, and close it when the row moves to `pm/archive.yaml`.
- **History keeps its own names.** If the project changes id schemes, rows in
  `pm/archive.yaml`, entries in `pm/log.md`, notes in `context/`, and titles of
  closed external issues stay exactly as written. A `depends_on` may then name an
  old code — it is the id the archive is indexed by. Rewriting history to the
  new scheme is not a cleanup, it is a falsification.

**Without an external tracker**, `pm/` mints the id: one project-wide sequence,
never a family per type, never reused.

## Planning Gate

**Scale the plan to the work.** The gate exists so that substantial work is
agreed before it is built, not so that every change acquires paperwork.

- **A contained fix changes nothing a user or caller can observe** — a crash, a
  bad log line, a build break, a broken developer script. One clear cause,
  verifiable by a test or a reproduction: it needs a tracker row, and then it
  can be done. Say what you are about to do, and do it.
- **If output, status, or stored data changes, it needs a confirmed plan** under
  `pm/issues/{slug}/` before implementation — as does anything spanning several
  components or costing more than an hour or so. If you are unsure which side of
  the line a task is on, it is this one.

  The line is deliberately drawn at *observable change*, not at size or
  confidence. "One clear cause, small blast radius, I can test it" describes
  almost every bug fix ever attempted, including the ones that change a status
  code, a rounding rule, or a default — so a gate built on that phrasing has an
  escape hatch that is always open.
- **Confirm declared dependencies are `done`** — open ones in
  `pm/tracker.yaml`, closed ones in `pm/archive.yaml`. A `dropped` dependency is
  **not** satisfied. **A row's status can lag the code**, though: nothing forces
  the close-out into the session that lands the implementation, and a
  dependency has been merged while its row still read `planning`. Before
  treating one as unmet, grep the code and migrations for what it was supposed
  to produce.
- **Inspect every affected table, constraint, relationship and nearby code path
  before changing persistence behaviour.** This one does not scale down.
- The plan defines scope by observable behaviour, affected components, and
  verification. **A sequence diagram is required only when interactions,
  integrations, or process ordering are changing** — not for every fix.
- **The plan's scope is the whole scope.** Nothing outside it gets built and
  nothing inside it gets silently skipped. If the work has to depart from it,
  update the plan and re-confirm before continuing.

## Working Discipline

Each of these is here because it actually went wrong.

**Measure a causal claim before writing it into `context/`, and re-measure one
you are about to act on.** A mechanism that *would* explain a symptom is not
evidence that it does. A plausible explanation for a slow test suite once read
exactly right, had been repeated twice, and was false — and it had already aimed
the work at the wrong fix while the real lever sat untried. Prefer a number to a
narrative: a timing, a count, a query, the tool's own source.

**A rule read off one reference document is a rule about that document.** A
layout rule confirmed against a reference document held for every example anyone
had seen, then broke on the first case where its grouping key was degenerate —
one group, or every group of size one. Before generalising from an example, look
for that case, and express the rule as a property of the data rather than as a
list of the instances seen so far.

**A new rule must reproduce the existing worked example before it may claim to
replace or generalise an older one.** The examples in
`context/document-writer-only/examples/` are the regression suite for the
conventions. Asserting that an existing rule is "a specialisation" of a new
abstraction is a claim with a cheap test: run the new rule against the worked
example and check it yields the same output. Skipped once, and the worked
example would have falsified the claim immediately.

**An explicit written rule outranks in-the-moment reasoning.** When analysis
points somewhere other than what a `context/` file already says, the written
rule wins by default: state the tension, propose the change, let the user
decide. A framework whose rules bend to whoever is holding it produces different
answers on different days.

**A surprising derivation result means "check the rule" first, "check the input"
second.** When something yields far less or far more than expected, the first
hypothesis is that the rule being applied is wrong; the scope of the input is
the second. Reaching for the input explanation first turns into defending a
broken rule.

**Walk every branch to a terminal state before calling a process model done.**
For each path, including every failure branch, ask what the actor does next. A
branch that stops with no continuation, a decision whose input is never
produced, or a step that proceeds regardless of a result it depends on are all
modelling bugs, and all invisible if only the happy path is read.

**Read current sources before recommending an architecture or an API, not
after.** A recommendation assembled from memory and then checked has already
anchored. Do not guess a framework's behaviour: inspect the installed version or
its current documentation.

**Preserve behaviour outside the confirmed scope.** Do not bundle cleanup,
renaming, or architecture changes into a contained fix.

**In a design conversation, recommend in prose.** Give the recommendation and
the reasoning as text and let the user react. Reserve structured multiple-choice
prompts for a genuine fork where work cannot continue. When the user restates
their framing a second time, build on their version instead of re-deriving it.

**Continue through to verification** unless the user asked only for analysis,
planning, review, or documentation.

## Version Control

- **Stage by path, never `git add -A` or `git add .`.** The worktree routinely
  carries several issues in flight at once — a feature, an unrelated fix, and
  `pm/` bookkeeping can all sit uncommitted beside the task at hand. Name the
  files the task actually touched and leave the rest modified.
- **The commit message carries `Refs {id}`.** When the work genuinely has no
  issue, say so in the message rather than leaving the reader to wonder.
- **Commit and push only when the user asks** — and push only when "push" was
  said, not merely "commit".
- **Record the branching model here, once.** Trunk-only (commit straight to
  `main`, no pull requests) and branch-per-issue are both defensible; not
  saying which is not. An agent left to guess will branch "to be safe", which on
  a trunk-only project leaves work stranded on the remote until someone notices.
  _This project:_ `{trunk-only | branch-per-issue}`.

## Terminology Rule

When a concept has competing informal definitions across sources, **do not
invent our own.** Adopt the version used by the practitioner standard closest to
our context — SAP/Signavio for process architecture, since ERP clients are more
likely to have met that vocabulary — and cite it in the file that owns the
subject. Terminology defensible to a client beats terminology that is internally
tidy and unrecognised outside this repo. This project says **"Level"**, not
"Tier".

## Definition Of Done

1. **Verify.** The narrowest test or reproduction first, then the affected
   suite, then the formatter. For an artifact: rendered or reloaded and actually
   inspected, checked against its owning convention file.
2. **Reconcile** what was built against the plan, where there was one.
3. **Update durable ownership** — `context/index/map.md` when ownership moved,
   `context/index/decisions/` plus its index row when something architectural
   was settled, and the ERD whenever the schema changed — columns, types,
   constraints, keys, or relationships. Then answer:
   **what did this teach us, and where does it go?** — an entry appended to
   `context/gotchas.md`, an update to an existing owner in `context/`, or
   "nothing". "Nothing" is a valid answer; skipping the question is not.
4. **Move the row** from `pm/tracker.yaml` to `pm/archive.yaml` as `done` (or
   `dropped`, with a reason), with a concise summary of what was built and how
   it was verified.
5. **Append to `pm/log.md`**, newest first, tagged.
6. **Delete the capsule** from `pm/issues/`. Git history keeps the plan, found
   by slug (`git log --all --diff-filter=D -- '*{slug}*'`).
7. **Point `pm/active.json`** at the next issue, or clear it. Close the external
   issue, if one exists, with the same verification summary.

Steps 1–3 are what "done" means. The rest is bookkeeping, and it takes a minute
— but skipping straight to step 7 is what makes old work unreconstructable.

Pre-existing failures are reported separately. Never weaken a check, or alter
real client data, to satisfy verification.
