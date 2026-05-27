# Physical-First Principle

> LOAD target: `/aibdd-plan`, `/aibdd-spec-by-example-analyze`, `/aibdd-red`, and any skill that creates or consumes DSL physical mappings.

## Principle

Business DSL must be backed by a physical testing surface before it is used by RED phase.

Physical testability lives in boundary truth under `specs/`:

- provider operation contracts: `specs/contracts/`
- data/state/verifier truth: `specs/data/`
- dependency-edge test strategy: `specs/test-strategy.yml`
- part-derived DSL mapping: `specs/contracts/*.dsl.yml`, `specs/data/*.dsl.yml`
- shared boundary DSL mapping: `specs/shared/dsl.yml`

## Layer Order

| Layer | Meaning | Owner |
|---|---|---|
| Technical truth | boundary map, contracts, data/state, test strategy | `/aibdd-plan` |
| Flat DSL entry | `format`, `handler`, `target_part_path`, bindings | `/aibdd-plan` DSL synthesis |
| Preset handler | reusable step-def pattern such as `operation-invoke` | `/aibdd-plan` DSL synthesis + active `${PRESET_KIND}` |
| Business sentence | exact Gherkin-facing phrase in `format` | `/aibdd-plan` DSL synthesis, enriched by downstream examples |

## Flat Entry Mapping Contract

Each DSL entry must include enough typed mapping for `/aibdd-red`.

```yaml
dsl_steps:
  - name: openOrJoinRoom.operation-invoke
    format: 玩家 "{玩家Id}" 以房號 "{房號}" 開房或加入
    handler: operation-invoke
    target_part_path: specs/contracts/room.api.yml#/paths/~1rooms/post
    param_bindings:
      房號:
        target: specs/contracts/room.api.yml#/paths/~1rooms/post/requestBody/content/application~1json/schema/properties/roomNo
      玩家Id:
        target: specs/contracts/room.api.yml#/paths/~1rooms/post/requestBody/content/application~1json/schema/properties/playerId
    datatable_bindings: {}
```

Missing `target_part_path`, summary-only bindings, or untyped parameter bindings are hard failures.

## Red-Usability Rule

`/aibdd-red` should resolve:

```text
step prose
  -> unique DSL entry by format
  -> handler via active preset kind
  -> target_part_path
  -> param_bindings
  -> datatable_bindings
```

It must not parse plan prose, import production internals directly, invent mock channels, or guess fixture paths.

Handoff preserves legacy field names:

- `dsl_entry_id` ← `name`
- `matched_l1` ← `format`

## Anti-Patterns

- DSL entry has only `format` and `handler` but no typed bindings.
- `{placeholder}` appears in `format` but not in `param_bindings`.
- Then expected value has no binding target in `param_bindings` or `datatable_bindings`.
- External provider behavior is mocked without a dependency edge and test strategy.
- Same-boundary internal collaborator is modeled as an external stub.
- File upload API lacks fixture catalog, upload invocation, response verifier, state/file-store verifier, or missing-file behavior.
- Execute skills still require `${BOUNDARY_PACKAGE_DSL}` even when contracts/data corpus exists.

## Mock DSL Business Language Rule

### MR-1 `[MOCK]` Tag

Mock-setup Given steps must include visible `[MOCK]` after the keyword:

- Good: `Given [MOCK] 金流平台預設授權付款成功`
- Good: `And [MOCK] AWS 檔案儲存服務回報上傳成功`
- Bad: `Given payment gateway mock returns approved`

### MR-2 Business-Language Surface

`format` phrases and example datatable headers must avoid implementation terms:

- forbidden: `mock`, `stub`, `queue`, `fixture`, `harness`, `spy`, `MSW`, `stub_payload`, raw contract type names
- allowed: stakeholder-visible provider roles, such as `金流平台`, `檔案儲存服務`, `通知服務`

### MR-3 Datatable Headers

Datatable headers follow the same business-language rule. Prefer `評審`, `原因`, `金額`, `付款結果` over schema field names.

### MR-6 Datatable Schema Rule

Do not use generic key-value-bag headers such as `field | value` when the table represents business data. Use domain column names.

## Mock Interaction Pattern

External stub DSL entries should declare one interaction pattern:

- `arm-default`: provider has one default response
- `arm-by-input`: provider response depends on request fields
- `arm-sequence`: provider responses occur in order
- `observe-calls`: test verifies provider was called
- `overridden-impl`: test swaps an adapter implementation

The pattern belongs in the referenced test strategy entry or handler-specific binding truth, and must be traceable from `test-strategy.yml`.

## Relationship to Backend Presets

Backend entries should use handler names such as:

- `state-builder`
- `operation-invoke`
- `query`
- `operation-response-success-and-failure`
- `operation-response-success-readmodel`
- `state-verifier`

The active `${PRESET_KIND}` selects reusable step-definition pattern instructions; it does not replace typed `target_part_path` and bindings.

## Deprecated

- Function-package `specs/packages/NN-*/dsl.yml` as sole DSL truth
- Nested `L1` / `L2` / `L3` / `L4` entry blocks with `L4.source_refs` as the primary red contract
