# Phase 1 - Infra setup

- [x] 建立 DB 基礎結構：依 `specs/data/one-a-two-b-game.dbml` 建立 `GameModel`、`PlayerModel`、`SecretModel`、`GuessModel` 與 Alembic migration，讓 `tests/features/environment.py` 的 migration / truncate flow 可管理四個資料表。
- [x] 建立 API 基礎結構：依 `specs/contracts/one-a-two-b-game.api.yml` 建立 request / response schemas、錯誤 response helper，並讓 `app/main.py` 掛載 `/api/games` 相關 router。
- [ ] 建立 BDD 共用步驟基礎：在 `tests/features/steps` 補上合約 DSL 與資料 DSL 共用 step definitions，支援狀態建置、操作呼叫、回應驗證、資料狀態驗證。
- [ ] 建立測試資料 ID 對應規則：讓 feature 內的玩家代號 `p1` / `p2` 可由玩家名稱與角色解析為實際 player id，並在 context 中保存 API 回應與 DB 查詢結果。

# Phase 2 - 進入遊戲配對

## RED
- [x] 透過 `/aibdd-red-execute` 來撰寫 `specs/packages/01-雙人猜數字對戰/features/01-進入遊戲配對.feature` 的測試程式碼。
- [x] Looping 啟動一個獨立 Subagent，請他進行 `/aibdd-red-evaluate`。
  - [x] 輸入此 Feature 的 red evidence artifact paths。
  - [x] 若 evaluator 判定不合法，持續修正，然後重新啟動全新 evaluator subagent。
  - [x] 直到 evaluator 判定此 Feature 的 red 合法為止。

## GREEN
- [x] 透過 `/aibdd-green-execute` 讓 `specs/packages/01-雙人猜數字對戰/features/01-進入遊戲配對.feature` 轉綠。
- [x] 實作時必須參考 `specs/plans/001-1A2B雙人猜數字/implementation` 底下的設計與本 phase 的 implementation waves。

### Wave 1 - Pairing API surface
- [x] 建立 `GameRouter` 類別或 FastAPI router module，並實作 `POST /api/games` 對應的 `enterGame(request)` 行為。
- [x] 建立 `EnterGameRequest`、`EnterGameResponse`、`ErrorResponse` schema，套用 gameId 為 3-5 位英數、playerName 為 3 至 10 字元的驗證。
- [x] 建立 `EnterGameService` 類別，並實作 `enter_game(gameId, playerName)`，集中處理新遊戲、加入 P2、重複加入與已滿判斷。

### Wave 2 - Pairing persistence and phase transition
- [x] 建立 `GameRepository` 類別，並實作 `find_by_game_id`、`create_game`、`add_player_as_p2`，保存 P1 / P2 與 `WAITING_FOR_PLAYERS`、`SETTING_SECRETS` 狀態轉換。
- [x] 建立 `GameModel` 與 `PlayerModel` 類別，對應 games / players 資料表與 `(game_id, player_name)`、`(game_id, role)` 唯一性限制。
- [x] 建立明確錯誤映射，讓已滿遊戲回傳「該遊戲已滿，請選擇其他遊戲」，同名玩家重複加入回傳「同一玩家不得重複加入同一場遊戲」。

- [x] 進行回歸測試，確定所有測試都通過了，確認產出測試報告。
- [x] Looping 啟動一個獨立 Subagent，請他進行 `/aibdd-green-evaluate`。
  - [x] 輸入此 Feature 對應的 green / full-suite report artifact paths。
  - [x] 若 evaluator 判定不合格，持續修正，然後重新啟動全新 evaluator subagent。
  - [x] 直到 evaluator 判定 green 合法為止。

## Refactor
- [x] 進行 `/aibdd-refactor-execute`。
- [x] Looping 啟動一個獨立 Subagent，請他進行 `/aibdd-refactor-evaluate`。
  - [x] 輸入此 Feature 對應的 refactor / full-suite evidence artifact paths。
  - [x] 若 evaluator 判定不合格，持續修正，然後重新啟動全新 evaluator subagent。
  - [x] 直到 evaluator 判定 refactor 合法為止。

# Phase 3 - 設定秘密數字

## RED
- [x] 透過 `/aibdd-red-execute` 來撰寫 `specs/packages/01-雙人猜數字對戰/features/02-設定秘密數字.feature` 的測試程式碼。
- [x] Looping 啟動一個獨立 Subagent，請他進行 `/aibdd-red-evaluate`。
  - [x] 輸入此 Feature 的 red evidence artifact paths。
  - [x] 若 evaluator 判定不合法，持續修正，然後重新啟動全新 evaluator subagent。
  - [x] 直到 evaluator 判定此 Feature 的 red 合法為止。

## GREEN
- [x] 透過 `/aibdd-green-execute` 讓 `specs/packages/01-雙人猜數字對戰/features/02-設定秘密數字.feature` 轉綠。
- [x] 實作時必須參考 `specs/plans/001-1A2B雙人猜數字/implementation` 底下的設計與本 phase 的 implementation waves。

### Wave 1 - Secret setting endpoint and rules
- [x] 在已建立的 `GameRouter` 或 router module 上新增 `POST /api/games/{gameId}/secrets`，並串接 `SetSecretService.set_secret(gameId, playerId, secret)`。
- [x] 建立 `SetSecretService` 類別，並實作玩家必須屬於該遊戲、遊戲必須為 `SETTING_SECRETS`、P1 必須先於 P2 設定的規則。
- [x] 建立 `SecretNumberRules` 類別，並實作 `validate_four_unique_digits(value)` 與 `ensure_p1_then_p2_order(game, player)`。

### Wave 2 - Secret persistence and guessing transition
- [x] 在既有 `GameRepository` 上補上 `load_game_with_players_and_secrets(gameId)` 與 `save_secret(playerId, secret)`，保存 secret 並維持 `change_count = 0`。
- [x] 建立 `SecretModel` 類別，對應 secrets 資料表與 player 唯一 secret 的限制。
- [x] 在 P2 完成合法設定且 P1 已有 secret 時，將遊戲狀態更新為 `GUESSING`，並讓 response / state verifier 可觀察到此狀態。

- [x] 進行回歸測試，確定所有測試都通過了，確認產出測試報告。
- [x] Looping 啟動一個獨立 Subagent，請他進行 `/aibdd-green-evaluate`。
  - [x] 輸入此 Feature 對應的 green / full-suite report artifact paths。
  - [x] 若 evaluator 判定不合格，持續修正，然後重新啟動全新 evaluator subagent。
  - [x] 直到 evaluator 判定 green 合法為止。

## Refactor
- [x] 進行 `/aibdd-refactor-execute`。
- [x] Looping 啟動一個獨立 Subagent，請他進行 `/aibdd-refactor-evaluate`。
  - [x] 輸入此 Feature 對應的 refactor / full-suite evidence artifact paths。
  - [x] 若 evaluator 判定不合格，持續修正，然後重新啟動全新 evaluator subagent。
  - [x] 直到 evaluator 判定 refactor 合法為止。

# Phase 4 - 修改秘密數字

## RED
- [x] 透過 `/aibdd-red-execute` 來撰寫 `specs/packages/01-雙人猜數字對戰/features/03-修改秘密數字.feature` 的測試程式碼。
- [ ] Looping 啟動一個獨立 Subagent，請他進行 `/aibdd-red-evaluate`。
  - [ ] 輸入此 Feature 的 red evidence artifact paths。
  - [ ] 若 evaluator 判定不合法，持續修正，然後重新啟動全新 evaluator subagent。
  - [ ] 直到 evaluator 判定此 Feature 的 red 合法為止。

## GREEN
- [ ] 透過 `/aibdd-green-execute` 讓 `specs/packages/01-雙人猜數字對戰/features/03-修改秘密數字.feature` 轉綠。
- [ ] 實作時必須參考 `specs/plans/001-1A2B雙人猜數字/implementation` 底下的設計與本 phase 的 implementation waves。

### Wave 1 - Secret change endpoint and preconditions
- [ ] 在已建立的 `GameRouter` 或 router module 上新增 `PATCH /api/games/{gameId}/secrets/{playerId}`，並串接 `ChangeSecretService.change_secret(gameId, playerId, secret)`。
- [ ] 建立 `ChangeSecretService` 類別，並實作玩家必須已設定 secret、遊戲尚未進入 `GUESSING`、修改次數尚未達一次的規則。
- [ ] 在既有 `SecretNumberRules` 上補上 `ensure_before_guessing(phase)` 與 `ensure_change_count_less_than_one(secret)`，並重用 `validate_four_unique_digits(value)`。

### Wave 2 - Secret update persistence
- [ ] 在既有 `GameRepository` 上補上 `load_game_with_secret(gameId, playerId)` 與 `update_secret_and_increment_change_count(playerId, secret)`。
- [ ] 基於既有 `SecretModel` 調整 / 補強更新行為，確保合法修改會覆蓋自己的 `secret_value` 並將 `change_count` 加 1。
- [ ] 補上錯誤訊息映射：猜題階段後不得修改、玩家必須先設定秘密答案、秘密答案最多只能修改一次、格式不合法。

- [ ] 進行回歸測試，確定所有測試都通過了，確認產出測試報告。
- [ ] Looping 啟動一個獨立 Subagent，請他進行 `/aibdd-green-evaluate`。
  - [ ] 輸入此 Feature 對應的 green / full-suite report artifact paths。
  - [ ] 若 evaluator 判定不合格，持續修正，然後重新啟動全新 evaluator subagent。
  - [ ] 直到 evaluator 判定 green 合法為止。

## Refactor
- [ ] 進行 `/aibdd-refactor-execute`。
- [ ] Looping 啟動一個獨立 Subagent，請他進行 `/aibdd-refactor-evaluate`。
  - [ ] 輸入此 Feature 對應的 refactor / full-suite evidence artifact paths。
  - [ ] 若 evaluator 判定不合格，持續修正，然後重新啟動全新 evaluator subagent。
  - [ ] 直到 evaluator 判定 refactor 合法為止。

# Phase 5 - 提交猜測

## RED
- [ ] 透過 `/aibdd-red-execute` 來撰寫 `specs/packages/01-雙人猜數字對戰/features/04-提交猜測.feature` 的測試程式碼。
- [ ] Looping 啟動一個獨立 Subagent，請他進行 `/aibdd-red-evaluate`。
  - [ ] 輸入此 Feature 的 red evidence artifact paths。
  - [ ] 若 evaluator 判定不合法，持續修正，然後重新啟動全新 evaluator subagent。
  - [ ] 直到 evaluator 判定此 Feature 的 red 合法為止。

## GREEN
- [ ] 透過 `/aibdd-green-execute` 讓 `specs/packages/01-雙人猜數字對戰/features/04-提交猜測.feature` 轉綠。
- [ ] 實作時必須參考 `specs/plans/001-1A2B雙人猜數字/implementation` 底下的設計與本 phase 的 implementation waves。

### Wave 1 - Guess endpoint and scoring rules
- [ ] 在已建立的 `GameRouter` 或 router module 上新增 `POST /api/games/{gameId}/guesses`，並串接 `SubmitGuessService.submit_guess(gameId, playerId, guess)`。
- [ ] 建立 `SubmitGuessService` 類別，並實作遊戲必須為 `GUESSING`、玩家必須存在、對手 secret 必須存在的前置檢查。
- [ ] 建立 `GuessScoringRules` 類別，並實作 `validate_guess_format(guess)`、`ensure_guessing_phase(phase)`、`score(guess, opponentSecret)`，正確計算 A / B。

### Wave 2 - Guess persistence and finishing game
- [ ] 在既有 `GameRepository` 上補上 `load_game_with_opponent_secret(gameId, playerId)`、`save_guess(a, b, isWin)` 與 `finish_game_with_winner(playerId)`。
- [ ] 建立 `GuessModel` 類別，對應 guesses 資料表，保存 guess_value、a_count、b_count、is_win。
- [ ] 當 score 為 `4A0B` 時，將 guesses 記為 win、將 `games.winner_player_id` 設為猜測玩家，並將 `games.phase` 更新為 `FINISHED`。

- [ ] 進行回歸測試，確定所有測試都通過了，確認產出測試報告。
- [ ] Looping 啟動一個獨立 Subagent，請他進行 `/aibdd-green-evaluate`。
  - [ ] 輸入此 Feature 對應的 green / full-suite report artifact paths。
  - [ ] 若 evaluator 判定不合格，持續修正，然後重新啟動全新 evaluator subagent。
  - [ ] 直到 evaluator 判定 green 合法為止。

## Refactor
- [ ] 進行 `/aibdd-refactor-execute`。
- [ ] Looping 啟動一個獨立 Subagent，請他進行 `/aibdd-refactor-evaluate`。
  - [ ] 輸入此 Feature 對應的 refactor / full-suite evidence artifact paths。
  - [ ] 若 evaluator 判定不合格，持續修正，然後重新啟動全新 evaluator subagent。
  - [ ] 直到 evaluator 判定 refactor 合法為止。

# Phase 6 - Integration

- [ ] 執行完整 acceptance regression，確認四個 Feature 依序通過，且 Phase 2 至 Phase 5 的資料狀態不互相污染。
- [ ] 執行 OpenAPI 與 DB schema 對照檢查，確認 API schema、SQLAlchemy models、Alembic migration 與 `specs/contracts/one-a-two-b-game.api.yml`、`specs/data/one-a-two-b-game.dbml` 一致。
- [ ] 執行完整測試報告彙整，保留 red / green / refactor / full-suite evidence artifact paths，供後續 evaluator 與交付審查使用。
