# web-frontend preset — plan-time plugin contract

本檔以 human-readable 方式記載 web-frontend preset 之 plan-time 履約規則。

> 狀態：web-frontend preset 尚未實作 part_to_dsl plugin（`scripts/part_to_dsl.py` 不存在）。本檔承載 boundary invariants 與 per-handler plan-time 履約，作為 future plugin 作者之 SSOT。
>
> 對應的 runtime / red-execute handler doc（`handlers/*.md`）目前亦尚未建立，留作 follow-up。

## Boundary-level invariants

以下 4 條 invariant 對所有 handler 共同生效，plugin 構造 template 時須整體保證：

### I1 — Cross-process surfaces

所有 `mock-*` 與 `api-*` handlers 之 `callable_via` 必須解析到一個跨「瀏覽器 ↔ test-runner」程序邊界的 variant-defined surface。

nextjs-playwright variant 之 canonical v1 機制：Playwright `page.route` interception（DevTools protocol-backed），mock 狀態存於 test-runner 端 fixture closure。

**禁止**：先前允許之 dev-only `/__test__/*` HTTP endpoints 已 deprecated；mock 層**不得**位於受測 app 內（`src/mocks/**` 禁用）。variant 的 fixture 檔是 mock 狀態與行為的唯一信源。

### I2 — OpenAPI schema gate

mock 層必須以 Zod 對每筆 outgoing call 對 OpenAPI operation schema 做驗證；不合 schema 之 dispatch 自動 fail 測試。

此為 layer-level gate，**非**逐 scenario sentence 之檢查 — handler 端**不得**在 `l4_requirements` 重複宣告 schema 強制。

### I3 — Per-scenario reset

任何 mutate cross-process state 之 handler（`mock-state-given`, `api-stub`）必須宣告 per-scenario reset，由 variant 提供 reset hook。**狀態跨 scenario 漏出禁止**。

### I4 — Storybook contract granularity

UI handlers（`ui-action`, `ui-readmodel-then`）引用 component contract 須落在 **Story export 級**（如 `src/stories/Button.stories.ts::Primary`），而非元件檔本身。同元件不同狀態可能對應不同 story。

---

## Tier-1 handlers（always required）

### route-given

- **Required source**: `route_map`
- **Plan-time 履約**：
  - `callable_via` 解析到 route-navigator surface（目標頁面）。
  - `param_bindings` / `datatable_bindings` 覆蓋 route segment values、query parameters、hash（若 sentence 參數化）。
  - `source_refs.route` 指向 route map 內目標頁面條目；auth-required pages 須明示前置條件（此 handler **不**靜默注入 auth）。

### viewport-control

- **Required source**: `test_strategy`
- **Plan-time 履約**：
  - `callable_via` 解析到 variant 配置之 viewport-controller surface。
  - `param_bindings` 覆蓋 width × height 或 variant 可解析之 named device profile id。
  - `source_refs.test_strategy` 指向 responsive-coverage policy（含 named device profiles 清單）。

### mock-state-given

- **Required source**: `mock_implementation`, `data_model`
- **Plan-time 履約**：
  - `callable_via` 解析到 variant-defined mock-control surface 上之 fixture builder。
  - `param_bindings + datatable_bindings + default_value` 覆蓋 `source_refs.data` 中宣告的所有 required 欄位（defaults 須在 fixture truth 內宣告，**不可**綁定時心證）。
  - `source_refs.data` 指向 data-model truth（Zod schema）。

### time-control

- **Required source**: `test_strategy`
- **Plan-time 履約**：
  - `callable_via` 解析到 browser test-clock surface（Playwright 1.45+ `page.clock` / sinon fake timers / variant 等價物）。
  - `param_bindings` 覆蓋目標 instant、duration、timezone 或 named clock state。
  - `source_refs.test_strategy` 指向 test-strategy 內 browser-visible time 控制條目。

### ui-action

- **Required source**: `route_map`, `component_contract`
- **Plan-time 履約**：
  - `callable_via` 解析到 rendered page 之 UI driver verb（`click | fill | select | upload | press | drag | navigate-history`）。
  - `param_bindings` 引用 roles 或 labelled targets — `getByRole` / `getByLabel` / `getByTestId` / 明示 `name=` — **禁止**裸 CSS / class selector。
  - `source_refs.component` 指向具體 Story export（如 `Button.stories.ts::Primary`）；`source_refs.route` 指向該 interaction 所在 route。本 handler **不**擁有 assertion bindings。

### operation-response-success-and-failure

- **Required source**: `operation_contract_response`
- **Optional source**: `component_contract`
- **Plan-time 履約**：
  - `assertion_bindings` 標明預期 feedback class（`success | failure`）與（必要時）surface（`toast | inline-error | banner | status-pill`）。
  - `source_refs.contract` 指向定義成功 / 失敗邊界之 OpenAPI operation response semantics。
  - `callable_via` 讀「已 render 之 UI feedback 區」，**不**啟動新 interaction。

### ui-readmodel-then

- **Required source**: `route_map`, `component_contract`
- **Optional source**: `operation_contract_response`
- **Plan-time 履約**：
  - `assertion_bindings` 以 role / label / test-id / accessible-name 對應 UI targets；collection 斷言透過 role 語意（`role=row`, `role=listitem`）解析，**不可**用 nth-child positional CSS。
  - `source_refs.component` 指向目標 element 之 Story export（list/table 場景同理）。
  - `callable_via` 從「已 render 之 DOM」讀，**不**啟動新 operation。

---

## Tier-2 handlers（opt-in per package）

### api-stub

- **Required source**: `test_strategy`, `mock_implementation`
- **Optional source**: `provider_contract`
- **Plan-time 履約**：
  - `callable_via` 解析到 mock-implementation table 之 per-scenario override surface，scoped to 目標 `operationId`。
  - `param_bindings` / `datatable_bindings` 覆蓋 override 形態 — response status、body fixture、latency、response 序列、fault profile。
  - `source_refs.contract` 指向 OpenAPI operation truth（若有 provider contract）；per-scenario reset 為必要（見 invariant I3）。

### url-then

- **Required source**: `route_map`
- **Plan-time 履約**：
  - `assertion_bindings` 標明 URL aspect（`pathname | searchParams.{key} | hash`）與預期值。
  - `source_refs.route` 指向 route map 條目；pathname 斷言允許 segment-parameterized matching（當 route 宣告動態 segments）。
  - `callable_via` 從 `page.url()` 或 variant 等價 accessor 讀取。

### api-call-then

- **Required source**: `provider_contract`, `mock_implementation`
- **Plan-time 履約**：
  - `callable_via` 解析到 variant-defined call-recorder surface。
  - `assertion_bindings` 標明 call selector（`operationId` + ordinal 或 predicate）與預期 match 形態（method / path-params / body / query / headers）。
  - `source_refs.contract` 指向 OpenAPI operation truth（binding shape 用）；schema enforcement 屬 layer-level（見 invariant I2）。

### mock-state-then

- **Required source**: `mock_implementation`, `data_model`
- **Plan-time 履約**：
  - `callable_via` 解析到 variant-defined mock-control surface 之 verifier function。
  - `assertion_bindings` 以 data-model truth 所定義之欄位為 target；`param_bindings` 或 `datatable_bindings` 覆蓋 lookup identity。
  - `source_refs.data` 指向被驗證形態之 data-model truth。

---

## Eval-time 補強

以上履約為 plan-time 構造規範。當未來 web-frontend plugin 落地時，須由 `scripts/part_to_dsl.py` 在 `generate_templates` 內構造性保證；dsl_cli eval 跑的是 6 條 universal rules，不重複檢查 handler↔scheme 對應。
