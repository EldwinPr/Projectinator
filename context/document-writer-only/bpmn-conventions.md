# BPMN Conventions

Working reference for hand-drafting BPMN process diagrams (`docs/diagrams/bpmn-as-is.drawio`, `bpmn-to-be.drawio`) from client elicitation notes. Distilled from OMG BPMN 2.0 (`formal-11-01-03.pdf`); own words, spec sections cited inline for verification. Not a copy of the spec — read the spec directly for edge cases.

## Diagram types actually used here

BPMN defines Process (orchestration), Collaboration, and Choreography diagrams (§7). This project only needs the first two:

- **Process diagram** — one actor's internal flow, private and either non-executable (documenting) or executable (§7, "Private Business Processes"). This is what a single-pool, no-swimlane diagram is.
- **Collaboration diagram** — two or more Participants (Pools) exchanging Message Flows (§7, "Collaborations"). Use this whenever the process crosses an organizational boundary (client ↔ vendor, department ↔ department).

Choreography and Conversation diagrams are out of scope for this project — skip them.

## Diagram levels (this project's 3-tier scheme)

"Process levels" isn't a BPMN spec concept — it's an informal process-architecture convention, and sources disagree on the exact count and boundaries. Per this project's [terminology rule](../general-rules.md#terminology-rule), the underlying concepts below are cited to two recognized practitioner sources rather than invented — but **the specific 3-tier scheme itself, and the choice to use BPMN notation at every tier, is this project's own deliberate simplification**, not a claim that Signavio or Oracle define it this way. Say so explicitly if this is ever presented to a reviewer.

**What's cited:**
- Signavio: Level 0 is a landscape/overview of an organization's management, core, and support processes — **not itself a chain of sequential steps** ([Signavio, "Business Process Mapping Levels"](https://www.signavio.com/wiki/process-discovery/business-process-mapping-levels/)).
- Signavio + Oracle agree: the *chain* (a sequence of major end-to-end stages, e.g. order-to-cash) is **Level 1**, not Level 0 (Signavio, as above; Oracle: "a value chain is a high-level model that categorizes the generic value-adding activities of an organization" — [Oracle, "Process Modeling using BPMN 2.0"](https://www.oracle.com/ocom/groups/public/@otn/documents/webcontent/172298.pdf), discussed in [AVIO Consulting, "Business Architecture and Hierarchical Process Modeling"](https://avioconsulting.com/blog/business-architecture-and-hierarchical-process-modeling/)).
- Both sources also agree BPMN notation is meant to start appearing only at deeper levels (Signavio: "starts to appear" around Level 2; Oracle: BPMN applies from Level 3 onward) — **not** at the landscape/chain tier.

**What's this project's own simplification (deliberately diverging from both sources above, for a small team that doesn't benefit from maintaining two separate notations):**

- **Tier 1 — Landscape + Chain (merges Signavio/Oracle's top two levels).** One diagram: a single Pool for the organization, with Lanes categorizing processes as **Managerial / Main / Supporting** (Signavio's management/core/support split). The **Main** lane holds the value chain — the major end-to-end stages, positioned left-to-right in sequence. Every box is drawn as a **collapsed BPMN sub-process** (the small `+` marker), even though the cited sources say plain boxes are more typical here — this project uses BPMN notation uniformly across all tiers instead of switching notations partway through. **No connecting arrows between the chain boxes** — position implies order, this tier doesn't carry formal Sequence Flow semantics. A box's `+` marker means "this has (or will have) its own Tier 2 diagram," not that it's already been decomposed.
- **Tier 2 — Workflow areas.** A **separate diagram per Tier-1 box**, decomposing that one box only — not a single diagram covering the whole chain. Per Signavio's own wording, a Level 2 map shows what's "inside *a* larger end-to-end process" (singular) — so if Tier 1 has, say, six Main-lane boxes plus a Managerial box and a Supporting box, that's up to eight independent candidate Tier 2 diagrams, each scoped to one box. This tier is where Pools/Message Flow start to matter (a Tier-1 box that looked like one atomic step often turns out, on decomposition, to be a multi-party interaction — see the worked example below). Still built from collapsed sub-processes internally where a piece is complex enough to warrant its own further breakdown; plain tasks where it isn't.
- **Tier 3 (and beyond) — Detailed process maps.** Full operational BPMN: individual tasks, gateways, events, lanes for actual roles. **This is what `docs/diagrams/bpmn-as-is.drawio` and `bpmn-to-be.drawio` are**, for a process simple enough not to need a Tier 2 at all. When a Tier 2 diagram does exist, Tier 3 follows the **same strict rule as every tier above it: one diagram decomposes exactly one box from its parent, never more.** A four-box Tier 2 diagram does not get a single Tier 3 diagram covering all four — only the specific box(es) that are actually worth decomposing get their own Tier 3 page, and that page's end event hands off back into the parent diagram's flow (e.g. into the next sibling box) rather than re-showing the rest of the parent. This is not a Signavio rule — Signavio's own wording is looser ("*a* Level 2 map may show... inside *a* larger end-to-end process," describing typical content, not mandating strict 1:1 nesting) — it's this project's own tightening, validated by actually building it out (see `demo/restaurant-bpmn-levels.drawio`). The nesting goes as deep as the real process needs — a Tier 4, Tier 5, etc. box is the same pattern recursing further, there's no fixed ceiling.

**Don't decompose until it's worth it** — same principle as `class-diagram-conventions.md`'s "small modules can stay undocumented": a trivial box at any tier doesn't need a child diagram just because the `+` marker exists as a *convention*; only build the next tier down when there's enough real internal complexity to justify a reader needing it. Most boxes at any given tier should stay leaves — only the ones actually worth drilling into get decomposed.

**Navigating between tiers**: when multiple tiers of the same process live together in one `.drawio` file (one page/tab per diagram), give a box that has a child diagram a distinguishing fill (e.g. light blue, `fillColor=#dae8fc;strokeColor=#6c8ebf;`) and a draw.io internal page link to that page, plus a "back to parent" link on the child page — see [draw.io shape mapping](#drawio-shape-mapping) for the exact link syntax. Leaf boxes stay unlinked and undecorated; the fill color is the only signal for "this has more detail," so don't apply it to a box that doesn't.

**Rollup diagrams — an optional alternative artifact for small processes.** Strict per-box recursion (above) is the *structural* rule and stays the default — it's what keeps individual diagrams legible as a process grows complex. But for a chain small enough to read legibly on one page (a handful of leaf tasks total, like the restaurant example), it's also fine to produce a **rollup**: a single diagram showing every leaf task expanded inline, generated by literally laying out the fully-decomposed detail in one place rather than clicking through tiers. This is *not* a replacement for the tiered pages — it's a second, additional artifact for when a reader wants the whole small process at a glance instead of navigating three pages to see four tasks. Two rules keep this from undermining the tiered structure:

- A rollup is only worth producing once the tiered decomposition is actually done — don't skip straight to a rollup as a shortcut past building the real tiers, or the recursive structure never gets built and this becomes the same "merge everything into one diagram" problem the strict rule exists to prevent.
- Label it explicitly as a rollup (e.g. a page/diagram named "Full detail (rollup)") so nobody mistakes it for a fourth tier in the hierarchy — it's a rendering of tiers already built, not a new level.

## Task types

All tasks share the rounded-rectangle shape; the icon in the top-left corner is what distinguishes them (§10.2.3.1). Pick based on who/what actually does the work. draw.io renders every task as `shape=mxgraph.bpmn.task2` with a `taskMarker=` attribute selecting the icon (verified against the installed draw.io Desktop's shape library, see [draw.io shape mapping](#drawio-shape-mapping) below):

- **User task** — a human performs the task at a screen/form, tracked by a system task list (§10.2.3.1, "User Task"). Use for anything done inside the ERP UI: filling a form, approving a record, reviewing a screen. `taskMarker=user`.
- **Manual task** — a human does the work with no system involvement at all, not tracked by any engine (§10.2.3.1, "Manual Task"). Use for physical/offline steps: signing a paper, physically inspecting goods, a phone call with no logging. `taskMarker=manual`.
- **Service task** — an automated system/service does the work, no human involved (§10.2.3.1, "Service Task"). Use for automated jobs, integrations, calculations the system does on its own. `taskMarker=service`.
- **Script task** — like a service task but specifically "a script the engine executes" (§10.2.3.1, "Script Task"). In practice, treat as a Service task unless the client explicitly distinguishes "the system runs a script" from "the system calls a service" — usually not worth the distinction in elicitation-level diagrams. `taskMarker=script`.
- **Business rule task** — the process hands off to a rules engine/decision table and gets a decision back (§10.2.3.1, "Business Rule"). Use when a business calls out an explicit rule set (e.g., "the system decides which approval tier applies based on amount"). `taskMarker=businessRule`.
- **Send task** — fires a message to another participant and immediately completes (§10.2.3.1, "Send Task"). Use for one-way notifications: send a Sales Order to the finance API, email a confirmation. `taskMarker=send`.
- **Receive task** — waits for a message to arrive from another participant before completing (§10.2.3.1, "Receive Task"). Use when the process is blocked waiting on external input; a Receive task with no incoming Sequence Flow can start the process (see Events below). `taskMarker=receive`.
- **Abstract/plain task** (no icon) — use when the type genuinely isn't known yet during elicitation, or doesn't matter for the diagram's purpose. Don't leave this as a lazy default — pick a real type once it's known. `taskMarker=abstract`.

If unsure between User and Service: ask "does a person look at a screen for this step?" Yes → User task. No → Service task.

Sub-process / call activity / transaction are the same base task shape with a structural attribute instead of a `taskMarker`: `bpmnShapeType=subprocess` (embedded sub-process, collapsed or expanded via `isLoopSub`), `bpmnShapeType=call` (Call Activity — invokes a reusable global process), `bpmnShapeType=transaction` (Transaction sub-process, §10.6). Rare in elicitation-level diagrams — reach for these only when the client explicitly describes a reusable sub-flow or a multi-step unit that must all succeed or all roll back.

## Gateway types

Gateways are diamonds; they control how Sequence Flow tokens converge and diverge (§10.5). draw.io renders every gateway as a diamond (`shape=mxgraph.bpmn.gateway2`, `perimeter=rhombusPerimeter`) with a `symbol=` attribute selecting the marker glyph inside it. Four kinds matter here:

- **Exclusive (XOR)** — diverging: exactly one outgoing path is taken, decided by a condition (§10.5.2). Converging: any arriving token passes through, no wait. This is an if/else decision. `symbol=exclusiveGw` (diamond with an X) or `symbol=none` (bare diamond) — pick one style and stay consistent within a diagram; draw.io's own palette defaults to the marked version.
- **Parallel (AND)** — diverging: all outgoing paths are taken simultaneously. Converging: waits for *all* incoming paths before continuing (§10.5.4). Use for "these things happen at the same time" / "these things must all finish before continuing" — a genuine fork/join, not a decision. `symbol=parallelGw` (diamond with a +).
- **Inclusive (OR)** — diverging: one or more outgoing paths are taken, each independently evaluated by its own condition (§10.5.3). Converging: waits for all *currently active* branches to arrive (more complex synchronization than Exclusive or Parallel). Use only when a step can trigger multiple simultaneous but conditional branches (e.g., "notify by email AND/OR SMS depending on preferences, could be both, could be one"). Rare in practice — reach for Exclusive or Parallel first; only use Inclusive when the process genuinely has this "zero or more of these branches" shape. `symbol=general;outline=end` (diamond with an open circle).
- **Event-based** — diverging only: the branch taken is decided by *which event happens first* (a message arrives, a timer fires), not by evaluating data (§10.5.6). Each outgoing path must lead to an Intermediate Event or Receive Task, not a Task. Use for "we wait to see what happens next" scenarios — e.g., "either the customer responds within 3 days (message) or the request times out (timer)." `symbol=multiple;outline=boundInt` (diamond with a pentagon outline).

Decision heuristic: business rule/condition on data → Exclusive. Things literally happen together → Parallel. Racing external triggers decide the path → Event-based. Multiple independent yes/no conditions can co-fire → Inclusive (last resort).

Complex gateway (§10.5.5, arbitrary activation conditions) exists in the spec — and in draw.io's palette as `symbol=complexGw` — but essentially never shows up in a business-elicitation diagram; omit it from the toolkit unless a process genuinely can't be expressed with the four above. draw.io also offers exclusive/parallel event-based variants (`outline=standard;symbol=multiple` and `outline=standard;symbol=parallelMultiple`) — spec-legal but niche enough to skip here.

## Event types

Events are circles; border thickness marks Start (thin) vs Intermediate (double) vs End (thick) (§10.4). The icon inside marks the trigger/result. draw.io renders every event as `shape=mxgraph.bpmn.event` with two attributes doing the work: `outline=` picks the border style (which position/interrupt-behavior it is) and `symbol=` picks the trigger icon:

- **Start event** — where the process instance begins; no incoming Sequence Flow (§10.4.2). `outline=standard` (thin single border).
  - **None** (no icon) — process starts by some unmodeled/manual trigger ("someone begins the process"). Default when the trigger isn't a message or timer. `symbol=none`.
  - **Message** (envelope icon) — process is kicked off by an incoming message/request (§10.4.2, Table 10.84). Use when a process starts because another participant sends something — a customer submits a request, another pool's Send task targets this one. `symbol=message`.
  - **Timer** (clock icon) — process starts on a schedule or at a specific time/date (§10.4.2, Table 10.84). Use for periodic/scheduled processes (e.g., "every Monday, generate the weekly report"). `symbol=timer`.
- **End event** — where a path of the process terminates; no outgoing Sequence Flow (§10.4.3). `outline=end` (thick single border).
  - **None** (no icon) — plain completion, nothing further happens. `symbol=none`.
  - **Message** (filled envelope) — sends a message as the process concludes (§10.4.3, Table 10.88). Use when finishing the process implies notifying someone. `symbol=message`.
  - **Error** (lightning-bolt icon) — process ends abnormally with a named error, caught by a matching boundary Error event elsewhere (§10.4.3, Table 10.88). Use to mark abnormal/failure termination paths. `symbol=error`.
  - **Terminate** (filled black circle) — immediately ends the *entire* process instance, cancelling all other active paths, not just this one (§10.4.3). Use sparingly — only for a genuine "abort everything now" ending, not a normal completion. `symbol=terminate`.
- **Intermediate event** — something happens mid-process without starting or ending it (§10.4.4). Two placements: inline in normal flow (catch or throw — `outline=catching` / `outline=throwing`, both double-border), or attached to a task/sub-process boundary (catch only — represents exception handling — `outline=boundInt` interrupting / `outline=boundNonint` non-interrupting, both double-border but interrupting is solid and non-interrupting is dashed).
  - **Message** — inline: waiting to receive, or sending, a message mid-process. On a boundary: interrupts or doesn't interrupt the attached activity if a message arrives while it's running (§10.4.4, Tables 10.89–10.90). Use for "waiting on a reply" or "an update arrives while this step is in progress." `symbol=message`.
  - **Timer** — inline: a wait/delay before continuing. On a boundary: a timeout on the attached activity (e.g., "if not approved within 3 days, escalate") (§10.4.4, Tables 10.89–10.90). `symbol=timer`.
  - **Error** — boundary only, always interrupting (`outline=boundInt`) — catches a named error thrown elsewhere in the attached activity and reroutes the flow to an exception path (§10.4.4, Table 10.90, "Error"). This is the standard "if something goes wrong in this step, branch to error handling" pattern. Not valid inline in normal flow. `symbol=error`.

For elicitation-level diagrams, None/Message/Timer/Error(/Terminate for end) cover nearly everything. Skip Escalation, Signal, Conditional, Link, Compensation, Cancel unless a specific requirement clearly needs one — they exist in both the spec (§10.4.5) and draw.io's palette (`symbol=escalation`, `symbol=signal`, `symbol=conditional`, `symbol=link`, `symbol=compensation`, `symbol=cancel`) but rarely surface in business-process elicitation.

## Pools and lanes

- **Pool = one Participant** — a distinct organization, system, or external party in the process (§9.2). One pool per company/department/external system that has its own process. A pool MAY be a "black box" (no internal detail, just a boundary) when the other side's internals aren't known or relevant — common for as-is diagrams of external parties.
- **Lane = sub-partition within a pool's process** — typically one lane per role, sub-department, or system component inside that participant (§9.2.2, §10.7). Lanes never cross pool boundaries; a Sequence Flow can cross lanes within a pool but never cross into another pool.
- **Sequence Flow** stays inside a single pool (connects activities within the same participant's process). **Message Flow** (§9.3) is the only connector allowed *between* pools — it represents a message/handoff crossing the organizational boundary.
- Rule of thumb when drafting: if two steps are done by the same organization but different people/roles, use lanes in one pool. If they're done by different organizations/systems, use separate pools connected by Message Flow.
- In draw.io, use the **generic Pool container** (`style="swimlane;html=1;childLayout=stackLayout;resizeParent=1;resizeParentMax=0;horizontal=0;startSize=20;horizontalStack=0;whiteSpace=wrap;"`, `value="<Participant name>"`), not the BPMN-specific `mxgraph.bpmn.swimlane` stencil — `childLayout=stackLayout` auto-stacks child Lanes top-to-bottom and auto-resizes the Pool to fit them, which avoids hand-computing each lane's `y` offset and pool height (a real source of overlap bugs when authoring by hand — see `demo/restaurant-bpmn-levels.drawio` for a worked example that hit and fixed this). Lanes are children of the Pool using the plain `style="swimlane;html=1;startSize=20;horizontal=0;"`, `value="<Lane name>"`, each given a `height` but no `y` (the parent's stack layout positions them). `horizontal=0` lays lanes as horizontal bands (process reads left-to-right within each lane — the usual BPMN orientation); `horizontal=1` gives vertical lanes instead. The nesting (Lane inside Pool) is what distinguishes Pool from Lane, not the stencil — both still use the generic `swimlane` style, just with `childLayout=stackLayout` only on the outer Pool.

## As-is vs to-be

Same notation, same element vocabulary for both — the difference is process, not syntax:

- **As-is**: drawn directly from raw elicitation notes/interviews, warts and all — captures what actually happens today, including undocumented workarounds, manual steps, and inconsistencies between what different stakeholders describe. Don't "clean up" contradictions found in elicitation; flag them for follow-up instead of silently resolving them in the diagram.
- **To-be**: the converged, redesigned version after gaps/inefficiencies in the as-is are discussed and resolved with the client. Only diagram what's been confirmed — don't design speculative process improvements into the to-be diagram without client sign-off.

## draw.io shape mapping

This project's `drawio` skill (`.claude/skills/drawio/SKILL.md`) authors BPMN as hand-written draw.io XML (Mermaid has no native BPMN diagram type). The style strings below were extracted directly from the installed draw.io Desktop app's bundled shape library (`app.asar`, BPMN palette definitions) — not from `search_shapes` (that tool needs the separate drawio-mcp MCP server, which isn't installed in this environment) and not guessed. Re-verify against the installed app if draw.io Desktop is ever updated to a version with a different shape library.

**Tasks** — `shape=mxgraph.bpmn.task2;rounded=1;taskMarker=<marker>;`

| BPMN task type | `taskMarker=` |
|---|---|
| User | `user` |
| Manual | `manual` |
| Service | `service` |
| Script | `script` |
| Business Rule | `businessRule` |
| Send | `send` |
| Receive | `receive` |
| Abstract / plain | `abstract` |

Sub-process/call/transaction use `bpmnShapeType=subprocess` / `call` / `transaction` on the same base shape instead of `taskMarker`. **Collapsed sub-process** (the tier-1/tier-2 building block above): `shape=mxgraph.bpmn.task2;rounded=1;bpmnShapeType=subprocess;isLoopSub=1;` — renders with the small `+` marker. Note: this rendered with a **dashed** border in the installed app rather than the solid border the BPMN spec uses for a collapsed sub-process (only the `+` marker itself is spec-correct) — flagged as unverified against the spec, not confirmed as correct, just confirmed as what this style string actually produces.

**Gateways** — `shape=mxgraph.bpmn.gateway2;perimeter=rhombusPerimeter;symbol=<symbol>;`

| Gateway type | `symbol=` | notes |
|---|---|---|
| Exclusive | `exclusiveGw` | or `none` for a bare diamond |
| Parallel | `parallelGw` | |
| Inclusive | `general` | plus `outline=end` |
| Complex | `complexGw` | out of scope for this project's diagrams |
| Event-based | `multiple` | plus `outline=boundInt` |

**Events** — `shape=mxgraph.bpmn.event;perimeter=ellipsePerimeter;outline=<outline>;symbol=<symbol>;`

`outline=` sets position/border:

| Position | `outline=` |
|---|---|
| Start | `standard` |
| End | `end` |
| Intermediate, inline, catching | `catching` |
| Intermediate, inline, throwing | `throwing` |
| Boundary, interrupting | `boundInt` |
| Boundary, non-interrupting | `boundNonint` |

`symbol=` sets the trigger icon: `none`, `message`, `timer`, `error`, `terminate` (end only), plus the skip-by-default ones — `escalation`, `signal`, `conditional`, `link`, `compensation`, `cancel`, `multiple`, `parallelMultiple`.

**Pools/Lanes** — Pool: `swimlane;html=1;childLayout=stackLayout;resizeParent=1;resizeParentMax=0;horizontal=0;startSize=20;whiteSpace=wrap;`. Lane (child of Pool): `swimlane;html=1;startSize=20;horizontal=0;`. Not the BPMN-specific `mxgraph.bpmn.swimlane` stencil — see "Pools and lanes" above for why (`childLayout=stackLayout` auto-stacks and auto-resizes, avoiding manual `y`-offset math).

**Data objects** — `shape=mxgraph.bpmn.data2;` plus `bpmnTransferType=none|input|output` (Data Object / Data Input / Data Output), `isCollection=1` for a multi-instance/collection marker.

**Flows/connectors**:

| Connector | style |
|---|---|
| Sequence Flow | `edgeStyle=elbowEdgeStyle;endArrow=blockThin;endFill=1;` |
| Conditional Sequence Flow | Sequence Flow + `startArrow=diamondThin;startFill=0;` (open diamond at source) |
| Default Sequence Flow | Sequence Flow + `startArrow=dash;` (slash mark at source) |
| Message Flow | `dashed=1;dashPattern=8 4;endArrow=blockThin;endFill=1;startArrow=oval;startFill=0;` |
| Association | `dashed=1;dashPattern=1 4;endArrow=none;startArrow=none;` (or `endArrow=open` for a directed association) |

Anything not covered above (Text Annotation is just a plain `text;` shape with no BPMN-specific stencil; Group is a generic dashed-rectangle container) — open the draw.io desktop app's "BPMN" shape panel and inspect directly rather than guessing.

**Inter-page links** (for multi-tier files, see "Navigating between tiers" above) — verified against draw.io's own XSD schema and source strings, not guessed: a cell is only clickable-to-another-page if it's wrapped in a `<UserObject>`, not a plain `<mxCell>` — `mxCell` has no `link` attribute in the schema.

```xml
<UserObject id="SomeId" label="Box Label" link="data:page/id,TARGET_PAGE_ID">
  <mxCell style="..." vertex="1" parent="...">
    <mxGeometry .../>
  </mxCell>
</UserObject>
```

`TARGET_PAGE_ID` is the `id` attribute of the target `<diagram>` element (give each page tab an explicit, memorable `id` when authoring, e.g. `id="tier2page"`, rather than relying on an auto-generated one). A static PNG/SVG export cannot prove the link actually works — page navigation is only testable by opening the file in draw.io itself.
