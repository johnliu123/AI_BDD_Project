# Execute Config Contract

This reference defines shared execute configuration for AIBDD Green.

## Target

- Public input is `target_feature_files`, a non-empty feature file list.
- Green may iterate over Scenarios inside those files, but must not accept a
  Scenario-only target as the external boundary.
- The target set must exactly match the driving Red handoff.

## Arguments Path

- `arguments_path` may be supplied by the caller.
- The default path is `${AIBDD_CONFIG_DIR}/arguments.yml`.
- Missing caller path and missing default path is a STOP condition.
- `specs/arguments.yml` is not a fallback.

## Core And Runtime References

- Core reference keys ending in `_REF` are paths and must be read directly.
- Boundary preset assets resolve through active `${PRESET_KIND}` to
  `.claude/skills/aibdd-core/assets/boundaries/<preset-kind>/`.
- `web-backend` is never resolved through a `backend` alias.
- Runtime commands, globs, report output, fixture behavior, and archive behavior
  come only from project-owned BDD stack runtime refs.

## DSL Corpus Drift

Green rebuilds current DSL truth using the same corpus and merge rules as
`aibdd-red-execute` Phase 3:

- `${CONTRACTS_DIR}/*.dsl.yml`
- `${DATA_DIR}/*.dsl.yml`
- `${BOUNDARY_SHARED_DSL}`

Merge order:

1. regular files first, in stable glob order
2. shared file last
3. entry `name` globally unique; first occurrence wins

Handoff fields map from flat entries:

- `dsl_entry_id` ← entry `name`
- `matched_l1` ← entry `format`
- `target_part_path` ← entry `target_part_path`

Green must not treat `${BOUNDARY_PACKAGE_DSL}` as DSL truth.

## Drift

Green compares the Red handoff with current DSL, core preset assets, and runtime
visibility before editing product code.

Any drift in `dsl_entry_id`, `matched_l1`, preset tuple, `target_part_path`,
step-def path, binding keys, runtime feature visibility, or step glob visibility
is a STOP condition.

DSL and preset drift routes to planning or BDD analysis. Runtime command, glob,
archive, fixture, and visibility drift routes to project-owned BDD stack config.
