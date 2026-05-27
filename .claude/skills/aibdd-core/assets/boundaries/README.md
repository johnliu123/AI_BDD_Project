# Boundary Preset Assets

1. 本目錄是 AIBDD core 針對 reusable boundary preset assets 的 SSOT。

2. Layout
   1. `shared/`
      1. cross-boundary shared template 與 shared trace schema。
      2. 只放 boundary-neutral guideline；不得放某一個 boundary 的 strategy 細節。
   2. `<boundary>/`
      1. 每個 boundary 自己擁有的 preset assets root。
      2. 目前已存在 `web-service/` 與 `web-frontend/`。
   3. `<boundary>/step-classification.yml`
      1. part / keyword / handler 的分類 SSOT。
   4. `<boundary>/plugin-contract.md`
      1. plan-time construction guarantee 與 preset invariant。
   5. `<boundary>/shared-dsl-template.yml`
      1. boundary-wide canonical shared DSL entries。
   6. `<boundary>/handlers/*.md`
      1. handler narrative 與 rendering guidance。
   7. `<boundary>/variants/*.md`
      1. stack-specific variant contract。
   8. `<boundary>/forms/*.tmpl`
      1. boundary-owned Example form template。
   9. `<boundary>/rules/*.md`
      1. shared legislation files；不得再把同一 boundary 的 rule-type delta 散落成獨立 entrypoint。
      2. web-service 以 `shared-given-law.md` 承載所有 rule type 共用的 `Given Block` construction SSOT。
      3. web-service 另拆 `given-delta-*.md` 承載各 rule type 的 `Given Delta` overlay。
      4. web-service 以 `shared-then-failure-law.md` 與 `shared-then-success-law.md` 承載 outcome-polarity 共用的 `Then Block` SSOT 與各 rule type 的 `Then Delta` 小節。
      5. `.feature` 內 `Given` block 的 `# rule:` 指向 shared Given law；`Then` / verifier block 的 `# rule:` 指向 shared Then law。
      6. arrangement worker 依 Rule headline prefix 載入對應的 `given-delta-*.md` 與 shared Then 小節。
   10. `schemas/`
       1. cross-boundary schema files。