# Workbook Conventions

How to read/extend the use case workbook (`docs/workbook.xlsx`).

## Sheet "Modules"

Columns: `Modul`, `Deskripsi`, `Owner`. One row per business module/domain (Sales, Finance, Planning, etc). This is a reference list for the `Modul` column on both use case sheets — not a hierarchy, just a lookup.

## Sheet "UC BPMN"

Use cases derived directly from a confirmed to-be BPMN task.

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
