from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class GameModel(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phase: Mapped[str] = mapped_column(String, nullable=False)
    winner_player_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    players = relationship(
        "PlayerModel",
        back_populates="game",
        cascade="all, delete-orphan",
        foreign_keys="PlayerModel.game_id",
    )


class PlayerModel(Base):
    __tablename__ = "players"
    __table_args__ = (
        UniqueConstraint("game_id", "player_name", name="uq_players_game_name"),
        UniqueConstraint("game_id", "role", name="uq_players_game_role"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"), nullable=False)
    player_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    game = relationship("GameModel", back_populates="players", foreign_keys=[game_id])


class SecretModel(Base):
    __tablename__ = "secrets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"), nullable=False)
    player_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.id"), nullable=False, unique=True
    )
    secret_value: Mapped[str] = mapped_column(String, nullable=False)
    change_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    set_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )


class GuessModel(Base):
    __tablename__ = "guesses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"), nullable=False)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"), nullable=False)
    guess_value: Mapped[str] = mapped_column(String, nullable=False)
    a_count: Mapped[int] = mapped_column(Integer, nullable=False)
    b_count: Mapped[int] = mapped_column(Integer, nullable=False)
    is_win: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    guessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
