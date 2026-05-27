# red-usable-flat-entry

Flat DSL entry schema consumed by `/aibdd-red-execute` and `/aibdd-green-execute`.

Normative schema detail also lives in
`aibdd-plan/04-dsl-synthesis/rules/01-dsl-entry-schema.md`.

## File Shape

- Top-level key is `dsl_steps: []` (not legacy `entries:`).
- Files live under `${CONTRACTS_DIR}/*.dsl.yml`, `${DATA_DIR}/*.dsl.yml`, and
  optionally `${BOUNDARY_SHARED_DSL}`.

## Entry Fields

Every entry MUST contain:

- `name` — globally unique id across the merged corpus
- `format` — exact Gherkin-facing step sentence with `{key}` placeholders
- `handler` — preset handler id (for example `operation-invoke`, `state-builder`)
- `target_part_path` — spec or code anchor for the instruction
- `param_bindings` — map of placeholder keys to `{ target: <uri> }`
- `datatable_bindings` — map of DataTable column keys to
  `{ target, required, default_value? }`

## Handoff Mapping

Execute skills preserve downstream handoff field names:

- `dsl_entry_id` ← `name`
- `matched_l1` ← `format`

## Merge Rules

Corpus merge matches `dsl_cli/catalog.py`:

1. load `${CONTRACTS_DIR}/*.dsl.yml` then `${DATA_DIR}/*.dsl.yml` in stable order
2. load `${BOUNDARY_SHARED_DSL}` last
3. reject duplicate `name` values across the merged corpus

## Target URI Schemes

Binding and `target_part_path` targets must use one of:

- OpenAPI spec anchor: `<file>#<json_pointer>`
- DBML spec anchor: `<file>#<table>` or `<file>#<table>.<column>`
- Code anchor: `code:<file_path>#<function_or_method>`
- Response probe: `response:<jsonpath>`
- Literal hint: `literal:<type>`
- Stub payload field: `stub_payload:<field_path>`

## Red Matching Rules

- Step prose MUST match exactly one entry `format` pattern after placeholder
  extraction.
- Every `{key}` in `format` MUST appear in `param_bindings`.
- DataTable columns MUST match `datatable_bindings` shape for the matched entry.
- `/aibdd-red` MUST NOT parse plan prose or invent bindings at runtime.

## Preset Resolution

- Active `${PRESET_KIND}` selects
  `.claude/skills/aibdd-core/assets/boundaries/<preset-kind>/`.
- Entry `handler` resolves handler docs inside that preset directory.
- Legacy nested `L4.preset` blocks are not part of this schema.

## Deprecated

- Function-package `${BOUNDARY_PACKAGE_DSL}` as sole DSL truth
- Legacy `entries:` top-level key with nested `L1` / `L2` / `L3` / `L4` blocks
- Handoff fields derived from `L4.source_refs` instead of flat entry fields
