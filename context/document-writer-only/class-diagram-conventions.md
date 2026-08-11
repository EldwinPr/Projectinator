# Class Diagram Conventions

How to draw the class diagram for a module. This is an **architecture diagram, not a UML domain model** — it shows the real classes that exist (or will exist) in a module's code and how they depend on each other, not conceptual domain entities with attributes/multiplicities.

## No fixed architectural pattern

This diagram doesn't assume a specific architecture — not a layered Model/Service/UI chain, not BCE (Boundary-Control-Entity), not hexagonal/ports-and-adapters, not anything else. Whatever the module's classes and their dependencies actually turn out to be once the stack and architecture are chosen, that's what goes on the diagram. Don't force a module's real structure into a pattern this file doesn't mandate — the point of the diagram is "these are the actual classes and what they call," not "here's how well the module conforms to architecture X."

Once this project's stack/architecture is settled, record the *actual* recurring shapes (a service layer, a repository, whatever the real codebase does) in `coding-conventions/` if a stable pattern emerges — this file stays about the diagramming convention, not about prescribing an architecture.

## Drawing rules

- **One box = one real class**, named exactly as it appears in code — `SalesOrderService`, not "Sales Order Service" or "Sales Order Service Class". If the class doesn't exist yet, don't put it on the diagram; draft it in the plan first.
- **Arrows show dependency direction only** — "calls" / "depends on", drawn as a plain open-arrowhead line. This is not a UML association/composition/aggregation diagram — don't add multiplicities, roles, or composition diamonds; none of that applies to a "what calls what" architecture map.
- **One diagram per module**, not one global diagram — a module's classes stay legible at module scope; a system-wide version of this diagram would just be `guide/component-conventions.md`'s job at a coarser grain.
- **Small modules can stay undocumented** until they grow enough classes that the dependency structure isn't obvious at a glance. Don't draft a diagram for a two-class module just for completeness.
- **Update at issue close time** when a new class is added to a module — same trigger as the ERD (see `document-writer-only/erd-conventions.md`), not a separate scheduled review.

## draw.io shapes

Verified against the installed draw.io Desktop's UML shape library (not from `search_shapes` — see the note in `document-writer-only/bpmn-conventions.md` for why):

| Element | style |
|---|---|
| Class box (plain, no attribute/method compartments — this diagram doesn't need them) | `rounded=0;whiteSpace=wrap;html=1;` |
| Dependency arrow ("calls"/"depends on") | `endArrow=open;endSize=12;html=1;` (drop the spec's `dashed=1` — a solid line reads better for "this is the real call chain," not a UML dependency's usual dashed/transient meaning) |

If a module's diagram ever needs to distinguish a strong compile-time dependency from a soft/late-bound one, use dashed vs solid rather than introducing new box shapes — keep the vocabulary small.
