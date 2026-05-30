---
description: Evaluate a completed AIBDD Refactor Worker run by checking strict dev constitution conformance and final full acceptance suite all pass.
metadata:
  source: project-level dogfooding
  user-invocable: true
name: aibdd-refactor-evaluate
---

# aibdd-refactor-evaluate

Evaluate whether a completed Refactor Worker run remained constitutional and behavior-safe.

<!-- VERB-GLOSSARY:BEGIN — auto-rendered from programlike-skill-creator/references/verb-cheatsheet.md by render_verb_glossary.py; do not hand-edit -->

## §1 REFERENCES

```yaml
references:
  - path: references/evaluate-input-contract.md
    purpose: Defines Refactor evaluate payload and artifact pointer requirements
  - path: references/evaluate-report-schema.md
    purpose: Defines Refactor evaluate PASS FAIL Veto report fields
  - path: references/dev-constitution-check.md
    purpose: Defines strict dev constitution conformance evidence and Veto standard
```

## §2 SOP

### Phase 1 — RECEIVE Refactor evidence
> produces: `$$payload`, `$$report_path`, `$$dev_constitution_path`, `$$code_scope`

1. `$$payload` = READ caller payload with `refactor_handoff` or explicit artifact pointers.
2. `$$report_path` = PARSE final full acceptance suite test report path per [`references/evaluate-input-contract.md`](references/evaluate-input-contract.md).
3. `$$dev_constitution_path` = PARSE resolved `${DEV_CONSTITUTION_PATH}` from payload or project config pointer.
4. `$$code_scope` = PARSE product codebase root and changed-file scope used for constitution checking.
5. ASSERT `$$report_path` exists; on failure STOP with `missing_refactor_full_suite_report`.
6. ASSERT `$$dev_constitution_path` exists; on failure STOP with `missing_dev_constitution_path`.
7. ASSERT `$$code_scope` is present; on failure STOP with `missing_constitution_check_scope`.

### Phase 2 — LOAD evidence
> produces: `$$test_report`, `$$dev_constitution`, `$$scoped_code`

1. `$$test_report` = READ `$$report_path`.
2. `$$dev_constitution` = READ `$$dev_constitution_path`.
3. `$$scoped_code` = READ product files in `$$code_scope`.
4. ASSERT `$$test_report` identifies the run as the full acceptance suite, not a target-only subset.
5. ASSERT `$$test_report` is runner-native evidence and contains no DSL mapping fields.

### Phase 3 — CHECK dev constitution strict
> produces: `$$constitution_findings`

1. `$$constitution_findings` = COMPUTE empty ordered list.
2. `$rules` = PARSE mandatory and prohibitive clauses from `$$dev_constitution` per [`references/dev-constitution-check.md`](references/dev-constitution-check.md).
3. LOOP per `$rule` in `$rules`
   3.1 `$violation` = JUDGE `$$scoped_code` against `$rule`.
   3.2 IF `$violation` == true:
       3.2.1 MARK `$$constitution_findings` with `$rule`
       END IF
   END LOOP
4. ASSERT constitution judgment is strict; no violated MUST or MUST NOT may be downgraded to advisory.

### Phase 4 — CHECK full suite all pass
> produces: `$$test_findings`

1. `$$test_findings` = COMPUTE empty ordered list.
2. `$failures_zero` = MATCH `$$test_report` has `0 failed`.
3. IF `$failures_zero` == false:
   3.1 MARK `$$test_findings` with `full_suite_failed`
4. `$errors_zero` = MATCH `$$test_report` has `0 errors`.
5. IF `$errors_zero` == false:
   5.1 MARK `$$test_findings` with `full_suite_error`
6. `$skip_safe` = MATCH `$$test_report` contains no scenario hidden by improper skip, xfail, deselect, or collection omission.
7. IF `$skip_safe` == false:
   7.1 MARK `$$test_findings` with `not_assertion_passed`

### Phase 5 — EMIT Refactor evaluation
> produces: `$$evaluation_report`

1. `$verdict` = DERIVE `PASS` when `$$constitution_findings` and `$$test_findings` are empty, else `FAIL`.
2. `$$evaluation_report` = RENDER report per [`references/evaluate-report-schema.md`](references/evaluate-report-schema.md) using `$$report_path`, `$$dev_constitution_path`, `$$code_scope`, `$$constitution_findings`, `$$test_findings`, and `$verdict`.
3. EMIT `$$evaluation_report` to caller.

## §3 CROSS-REFERENCES

- `/aibdd-refactor-execute` — Worker skill that produces the Refactor run evidence evaluated here.
- `/speckit-constitution` — owns changes to `${DEV_CONSTITUTION_PATH}` outside the evaluator.
