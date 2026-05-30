@ignore
Feature: 設定秘密數字
    Rule: 前置（狀態） - 遊戲必須已滿兩位玩家
        - 來源：若遊戲已經滿兩位玩家，則進入設定秘密數字階段。

        Scenario: 未滿兩位玩家時不得設定秘密答案
            Given 已存在遊戲 H12 且狀態為 WAITING_FOR_PLAYERS
            And 遊戲 H12 已有玩家 小明玩家 擔任 P1
            When 玩家 p1 在遊戲 H12 設定秘密數字 1234
            Then 錯誤訊息應為 遊戲必須已滿兩位玩家

    Rule: 前置（參數） - 秘密答案必須為 4 位數字
        - 來源：玩家需要設定一組 4 位數、數字不重複的答案。

        Scenario Outline: 拒絕不是 4 位數字的秘密答案
            Given 已存在遊戲 I12 且狀態為 SETTING_SECRETS
            And 遊戲 I12 已有玩家 小明玩家 擔任 P1
            And 遊戲 I12 已有玩家 小華玩家 擔任 P2
            When 玩家 p1 在遊戲 I12 設定秘密數字 <秘密數字>
            Then 錯誤訊息應為 秘密答案必須為 4 位不重複數字

            Examples:
                | 秘密數字 |
                | 123 |
                | 12345 |
                | 12A4 |

    Rule: 前置（參數） - 秘密答案數字必須不重複
        - 來源：答案的格式必須確認此 4 位數字不重複。

        Scenario Outline: 拒絕含有重複數字的秘密答案
            Given 已存在遊戲 J12 且狀態為 SETTING_SECRETS
            And 遊戲 J12 已有玩家 小明玩家 擔任 P1
            And 遊戲 J12 已有玩家 小華玩家 擔任 P2
            When 玩家 p1 在遊戲 J12 設定秘密數字 <秘密數字>
            Then 錯誤訊息應為 秘密答案必須為 4 位不重複數字

            Examples:
                | 秘密數字 |
                | 4444 |
                | 1123 |
                | 1223 |

    Rule: 前置（狀態） - P1 必須先於 P2 設定秘密答案
        - 來源：兩位玩家輪流設定答案，從 P1 開始，接著才輪到 P2。

        Scenario: P2 不得早於 P1 設定秘密答案
            Given 已存在遊戲 K12 且狀態為 SETTING_SECRETS
            And 遊戲 K12 已有玩家 小明玩家 擔任 P1
            And 遊戲 K12 已有玩家 小華玩家 擔任 P2
            When 玩家 p2 在遊戲 K12 設定秘密數字 5678
            Then 錯誤訊息應為 P1 必須先設定秘密答案

    Rule: 後置（狀態） - 格式不合法的秘密答案不得使玩家完成答案設定
        - 來源：答案的格式必須通過系統驗證，否則無法進入猜題階段。

        Scenario: P1 輸入不合法秘密答案後遊戲仍停留設定階段
            Given 已存在遊戲 L12 且狀態為 SETTING_SECRETS
            And 遊戲 L12 已有玩家 小明玩家 擔任 P1
            And 遊戲 L12 已有玩家 小華玩家 擔任 P2
            When 玩家 p1 在遊戲 L12 設定秘密數字 4444
            Then 錯誤訊息應為 秘密答案必須為 4 位不重複數字
            And 遊戲 L12 狀態應為 SETTING_SECRETS

    Rule: 後置（狀態） - 兩位玩家皆已設定答案的遊戲應進入猜題階段
        - 來源：當系統偵測到「兩位玩家皆已設定好答案」，即進入猜題階段。

        Scenario: P2 在 P1 已設定後完成設定使遊戲進入猜題階段
            Given 已存在遊戲 M12 且狀態為 SETTING_SECRETS
            And 遊戲 M12 已有玩家 小明玩家 擔任 P1
            And 遊戲 M12 已有玩家 小華玩家 擔任 P2
            And 玩家 p1 在遊戲 M12 已設定秘密數字 1234
            When 玩家 p2 在遊戲 M12 設定秘密數字 5678
            Then 回應遊戲狀態應為 GUESSING
            And 遊戲 M12 狀態應為 GUESSING
