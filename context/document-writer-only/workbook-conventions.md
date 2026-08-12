# Workbook Conventions

How to read/extend the use case workbook (`docs/workbook.xlsx`).

## Sheet "Modules"

Columns: `Modul`, `Deskripsi`, `Owner`. One row per business module/domain (Sales, Finance, Planning, etc). This is a reference list for the `Modul` column on both use case sheets — not a hierarchy, just a lookup.

## Sheet "UC BPMN"

Use cases derived from a confirmed to-be BPMN diagram — **not** one row per BPMN task box.

**Derivation rule**: one UC row per **User task** (the actor-facing entry point where a human
looks at a screen and does something) — `User`, `Nama Use Case`, `Modul` all describe that
actor and their goal. Any **Service / Business Rule / Send / Receive** tasks that fire
automatically as a direct consequence of that User task (no actor decision in between) get
folded into the same UC's `Deskripsi` as a numbered sub-flow, not given their own row — e.g. a
customer's single "scan to pay" action triggering generate-bill → send-payment-request →
receive-result → generate-receipt is **one** UC ("Process Payment"), not four. **Manual tasks**
(zero system involvement — cooking, physically walking somewhere) are excluded entirely; they
never become a UC since there's no system behavior to specify.

Rationale: a use case is a complete, actor-meaningful interaction, not an internal computation
step — "generate a receipt" is never something anyone sets out to do on its own. This was a
real correction made while deriving UCs for `context/document-writer-only/examples/restaurant-bpmn.drawio` — an initial pass
gave every BPMN task its own row (11 rows) before being consolidated to 5, one per User task.

Columns: `Kode` (UC-xx), `Nama Use Case`, `User` (actor), `Modul`, `Input`, `Deskripsi`, `Output`, `Entity/Objek Terkait` (comma-separated, feeds the Entities sheet — keep spelling/case consistent across rows).

`Kode` is unique across the whole workbook, not just this sheet.

## Sheet "UC Non-BPMN"

Same columns as "UC BPMN". Holds use cases that didn't originate from the BPMN diagram — promoted from `requests.md` once confirmed as a real, functional need.

`Kode` prefix `UC-N` (e.g. `UC-N01`) to keep these visually distinct at a glance; still unique workbook-wide, never reuses a `Kode` already used on "UC BPMN".

## Sheet "Entities"

Columns: `Entity yang dibutuhkan`, `Owner`, `ERD` (bool). Deduped list pulled from the `Entity/Objek Terkait` column on both "UC BPMN" and "UC Non-BPMN".

In Google Sheets, kept live via a formula unioning both ranges. `UNIQUE`/`ARRAYFORMULA`/`QUERY`/`FLATTEN` are Google Sheets-only and don't port to `.xlsx` as a live formula — refresh manually or via script if working from the `.xlsx` directly.

`Owner` filled in manually once the list generates. `ERD` marks whether the entity has made it into the ERD yet.

## Promotion rule

A request in `requests.md` only becomes a workbook row once it's confirmed as a genuine functional need — rejected/unclear requests stay in `requests.md` with a one-line reason, they never get a `Kode`.

## Out of scope for this workbook

UC-to-code traceability lives in `context/index/map.yaml`, not in this workbook. This workbook stays scoped to requirements and entities only.

## Editing `docs/workbook.xlsx` programmatically

Use the `xlsx` skill (`openpyxl` — no formulas live in this workbook, so `recalc.py` isn't
required, though it's harmless if LibreOffice is available in the environment; it wasn't in
this project's Windows dev setup — `AF_UNIX` missing — so don't assume it'll run).

**`openpyxl`'s `ws.max_row` goes stale across separate save/reload cycles** — appending via
`next_row = ws.max_row + 1` in one script invocation, saving, then doing the same in a later
*separate* invocation can silently overwrite an existing row instead of appending after it. Hit
this three separate times on the same file: it clobbered `UC-N01` on one append; a
"clear rows 2..max_row" refresh of the Entities dedup left stale duplicate rows behind because
`max_row` was also wrong at clear time; and a later cleanup pass found `UC BPMN` still carrying
6 blank trailing rows from an earlier rewrite that never got trimmed, plus the `Entities` sheet's
own header cell (`A1`) silently blanked during one of the rebuild scripts — headers are just as
vulnerable to this as data rows, not only append targets. Mitigation:
- After every write, immediately re-load the file fresh and print the affected sheet(s) to confirm rows landed where expected — never assume a write succeeded from the script's own return value alone.
- When clearing/rebuilding a sheet's data rows (e.g. refreshing the Entities dedup), clear a generously oversized range (rows 2–40, not `2..ws.max_row`) and explicitly `ws.delete_rows()` down to the real last row afterward, so no stale trailing rows survive a shrink.
- Re-write header cells explicitly as the last step of any rebuild script, after all row operations — don't assume a header survives a clear/rebuild cycle untouched.
- See `.claude/agents/workbook-xlsx-author.md` for the agent that applies all of this automatically.
