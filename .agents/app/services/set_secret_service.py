from app.models import GameModel, PlayerModel
from app.repositories.game_repository import GameRepository


class SetSecretError(Exception):
    def __init__(self, message: str, code: str = "SET_SECRET_ERROR", status_code: int = 400) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class SecretNumberRules:
    @staticmethod
    def validate_four_unique_digits(value: str) -> None:
        if (
            not isinstance(value, str)
            or len(value) != 4
            or not value.isdigit()
            or len(set(value)) != 4
        ):
            raise SetSecretError("秘密答案必須為 4 位不重複數字")

    @staticmethod
    def ensure_setting_phase_with_two_players(game: GameModel, players: list[PlayerModel]) -> None:
        if game.phase != "SETTING_SECRETS" or len(players) < 2:
            raise SetSecretError("遊戲必須已滿兩位玩家")

    @staticmethod
    def ensure_p1_then_p2_order(player: PlayerModel, p1_has_secret: bool) -> None:
        if player.role == "P2" and not p1_has_secret:
            raise SetSecretError("P1 必須先設定秘密答案")


class SetSecretService:
    def __init__(self, repository: GameRepository) -> None:
        self.repository = repository

    def set_secret(self, game_id: str, player_id: str, secret: str) -> dict[str, str]:
        game = self.repository.find_by_game_id(game_id)
        if game is None:
            raise SetSecretError("找不到遊戲", code="GAME_NOT_FOUND", status_code=404)

        players = self.repository.players_for_game(game)
        SecretNumberRules.ensure_setting_phase_with_two_players(game, players)
        SecretNumberRules.validate_four_unique_digits(secret)

        player = self._resolve_player(game, player_id)
        p1 = next((candidate for candidate in players if candidate.role == "P1"), None)
        p1_has_secret = p1 is not None and self.repository.secret_for_player(p1.id) is not None
        SecretNumberRules.ensure_p1_then_p2_order(player, p1_has_secret)

        self.repository.save_secret(game, player, secret)
        if self._all_players_have_secrets(players):
            self.repository.update_game_phase(game, "GUESSING")

        return {"gameId": game.game_id, "phase": game.phase}

    def _resolve_player(self, game: GameModel, player_id: str) -> PlayerModel:
        try:
            player_pk = int(player_id)
        except (TypeError, ValueError):
            raise SetSecretError("找不到玩家", code="PLAYER_NOT_FOUND", status_code=404)

        player = self.repository.player_for_game_by_id(game, player_pk)
        if player is None:
            raise SetSecretError("找不到玩家", code="PLAYER_NOT_FOUND", status_code=404)
        return player

    def _all_players_have_secrets(self, players: list[PlayerModel]) -> bool:
        return all(self.repository.secret_for_player(player.id) is not None for player in players)
