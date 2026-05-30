from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import GameModel, PlayerModel, SecretModel


class GameRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_game_id(self, game_id: str) -> GameModel | None:
        return self.session.scalar(
            select(GameModel).where(GameModel.game_id == game_id)
        )

    def create_game(self, game_id: str, player_name: str) -> tuple[GameModel, PlayerModel]:
        game = GameModel(game_id=game_id, phase="WAITING_FOR_PLAYERS")
        self.session.add(game)
        self.session.flush()
        player = PlayerModel(game_id=game.id, player_name=player_name, role="P1")
        self.session.add(player)
        self.session.flush()
        return game, player

    def players_for_game(self, game: GameModel) -> list[PlayerModel]:
        return list(
            self.session.scalars(
                select(PlayerModel)
                .where(PlayerModel.game_id == game.id)
                .order_by(PlayerModel.id)
            )
        )

    def add_player_as_p2(self, game: GameModel, player_name: str) -> PlayerModel:
        player = PlayerModel(game_id=game.id, player_name=player_name, role="P2")
        self.session.add(player)
        game.phase = "SETTING_SECRETS"
        self.session.flush()
        return player

    def player_for_game_by_id(self, game: GameModel, player_id: int) -> PlayerModel | None:
        return self.session.scalar(
            select(PlayerModel).where(
                PlayerModel.game_id == game.id,
                PlayerModel.id == player_id,
            )
        )

    def secret_for_player(self, player_id: int) -> SecretModel | None:
        return self.session.scalar(
            select(SecretModel).where(SecretModel.player_id == player_id)
        )

    def save_secret(self, game: GameModel, player: PlayerModel, secret: str) -> SecretModel:
        existing = self.secret_for_player(player.id)
        if existing is not None:
            return existing

        secret_record = SecretModel(
            game_id=game.id,
            player_id=player.id,
            secret_value=secret,
            change_count=0,
        )
        self.session.add(secret_record)
        self.session.flush()
        return secret_record

    def update_game_phase(self, game: GameModel, phase: str) -> None:
        game.phase = phase
        self.session.flush()
