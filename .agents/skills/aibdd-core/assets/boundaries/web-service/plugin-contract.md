# web-service preset — plan-time plugin contract

本檔以 human-readable 方式記載 web-service preset 之 part_to_dsl plugin 必須在構造期保證之履約規則。plugin 程式碼位於 `scripts/part_to_dsl.py`；本檔是 plugin 行為的規範敘事，二者語義需保持一致。

> 對應的 runtime / red-execute concerns 由 `handlers/*.md` 載；本檔只談 plan-time（template skeleton 構造）的履約。

## state-builder

- **Required source**: `data_model`
- **Plugin 構造保證**：
  - `target_part_path` 必須指向 DBML 規格內某 `table`（`<spec_file>#<table_name>`）。
  - 對該 table 之每個 column 各生一條 `candidate_binding`，target 為該 column 的 DBML anchor（`<spec_file>#<table>.<column>`）。
  - SEMANTIC 階段需做到：`param_bindings + datatable_bindings + default_value`（套用 `required:false` + `default_value` 後仍須由 scenario 提供者）必須 **100% 覆蓋該 table 之 NOT-NULL columns**。
  - 例外（不必涵蓋）：`[pk, increment]` 列、有明確 DBML `[default: ...]` 之列。
  - **時間戳例外不適用**：`created_at` / `updated_at` 等慣用欄位若 DBML 未宣告 `[default: ...]`，仍須由綁定提供，**不得**心證跳過。
  - **FK NOT-NULL 列必須直接綁定**：不允許「靠 lookup chain 推得」之省略。
  - 同一 scenario 涉多 table 時，per table 各一條 state-builder entry；FK 目標須由更早一條 builder 或同批 fixture 順序滿足。

## operation-invoke

- **Required source**: `operation_contract`
- **Plugin 構造保證**：
  - `target_part_path` 必須指向唯一一個 OpenAPI operation（`<spec_file>#/paths/<escaped_path>/<method>`）。
  - HTTP method、path、request body、query、headers 全部取自該 operation contract，不得心證。
  - `candidate_bindings` 涵蓋所有 required request inputs（path params + body schema properties with `required: true`）。
  - 此 handler **不**擁有 assertion 語義；任何 response 斷言一律改用 `operation-response-*` family entry。

## operation-response-success-and-failure

- **Required source**: `operation_contract_response`
- **Plugin 構造保證**：
  - `target_part_path` 指向 operation 之某個成功 response（典型為 `.../responses/200`），不可指向 schema 內節點。
  - `callable_via` 引用「已被 invoke handler 捕獲之 response」，**不**啟動新的 operation 呼叫。
  - 此 entry 用於判定整體 success/failure 結果分類（status 類或錯誤類訊號），不必綁定 payload 欄位。

## operation-response-success-readmodel

- **Required source**: `operation_contract_response`
- **Plugin 構造保證**：
  - `target_part_path` 指向 response 之 schema 節點（典型為 `.../responses/200/content/application~1json/schema`）。
  - `candidate_bindings` 每條 target 須走 **`response:` JSONPath scheme**（如 `response:$.roomNo`）；不得使用 spec anchor scheme。
  - `callable_via` 引用「已被 invoke 捕獲之 response」，**不**啟動新的 operation 呼叫。

## state-verifier

- **Required source**: `data_model`
- **Plugin 構造保證**：
  - 若來源為 `DbmlTablePart`，`target_part_path` 指向 DBML 規格內某 table（與 state-builder 同 scheme）。
  - 若來源為 relationship-derived part，`target_part_path` 指向 DBML 關係 anchor（如 `data/domain.dbml#ref:players.room_id>rooms.id`）。
  - relationship-derived verifier 只 fan-out 一條 `state-verifier` entry，不產 `state-builder` sibling。
  - relationship-derived verifier 的 `candidate_bindings` 只覆蓋關係兩端驗證所需的 identity / FK 欄位；不得退化成整張 table 欄位全掃。
  - SEMANTIC 階段需做到：`param_bindings` 或 `datatable_bindings` 覆蓋查找身份（identity 欄位）；assertion 欄位走 `datatable_bindings`。
  - 不得讀 `context.last_response` — verifier 永遠以 DB 為信源。

## time-control

- **Required source**: `test_strategy`
- **Plugin 構造保證**：
  - `target_part_path` 指向 test-strategy 文件內 time-control 區段（如 `test-strategy.md#time-control`）。
  - `candidate_bindings` 之 target 走 **`literal:` type-hint scheme**（如 `literal:iso8601-instant`）；具體時刻值由 Gherkin DataTable 直接餵入。
  - 本 handler 之 entry 本身屬 shared DSL（由 kickoff seeding 而非 part-driven 產生）；plugin 不直接構造它，但 plan 文件記述於此供參。

## external-stub

- **Required source**: `test_strategy`
- **Optional source**: `provider_contract`
- **Plugin 構造保證**：
  - `target_part_path` 指向 test-strategy 文件之 external-stub 區段（如 `test-strategy.md#external-stub/<resource>`）。
  - `candidate_bindings` 之 target 走 **`stub_payload:` field scheme**（如 `stub_payload:targetUserId`）。
  - 若該外部 provider 有 contract，`L4.source_refs.contract` 對應引用；否則僅以 test-strategy 為真。
  - 本 handler entry 屬 shared DSL，與 time-control 同。

## Eval-time 補強

以上履約為 plan-time 構造規範，並非 dsl_cli eval 規則。dsl_cli eval 跑的是 6 條 universal rules（format-params-cap、datatable-cap、schema-completeness、name-uniqueness、format-key-binding-bijection、target-uri-scheme-validity），不重複檢查 handler↔scheme 對應 — 後者由 plugin 構造性保證。
