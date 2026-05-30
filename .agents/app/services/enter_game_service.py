import re

from app.repositories.game_repository import GameRepository


class EnterGameError(Exception):
    def __init__(self, message: str, code: str = "ENTER_GAME_ERROR", status_code: int = 400) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class EnterGameService:
    GAME_ID_PATTERN = re.compile(r"^[A-Za-z0-9]{3,5}$")

    def __init__(self, repository: GameRepository) -> None:
        self.repository = repository

    def enter_game(self, game_id: str, player_name: str) -> dict[str, str]:
        self._validate_game_id(game_id)
        self._validate_player_name(player_name)

        game = self.repository.find_by_game_id(game_id)
        if game is None:
            game, player = self.repository.create_game(game_id, player_name)
            return {
                "gameId": game.game_id,
                "playerId": str(player.id),
                "role": player.role,
                "phase": game.phase,
                "message": "已建立新遊戲",
            }

        players = self.repository.players_for_game(game)
        if any(player.player_name == player_name for player in players):
            raise EnterGameError("同一玩家不得重複加入同一場遊戲")

        if len(players) >= 2 or game.phase in {"GUESSING", "FINISHED"}:
            raise EnterGameError(
                "該遊戲已滿，請選擇其他遊戲",
                code="GAME_FULL",
                status_code=409,
            )

        player = self.repository.add_player_as_p2(game, player_name)
        return {
            "gameId": game.game_id,
            "playerId": str(player.id),
            "role": player.role,
            "phase": game.phase,
            "message": "已加入遊戲",
        }

    def _validate_game_id(self, game_id: str) -> None:
        if not isinstance(game_id, str) or not self.GAME_ID_PATTERN.fullmatch(game_id):
            raise EnterGameError("遊戲 ID 必須為 3-5 位字母或數字")

    def _validate_player_name(self, player_name: str) -> None:
        if not isinstance(player_name, str) or not (3 <= len(player_name) <= 10):
            raise EnterGameError("玩家名稱必須為 3 至 10 字元")
