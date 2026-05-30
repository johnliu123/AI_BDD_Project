"""create one a two b tables

Revision ID: 20260530_0001
Revises:
Create Date: 2026-05-30
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260530_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "games",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("game_id", sa.String(), nullable=False),
        sa.Column("phase", sa.String(), nullable=False),
        sa.Column("winner_player_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("game_id", name="uq_games_game_id"),
    )
    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("game_id", sa.Integer(), sa.ForeignKey("games.id"), nullable=False),
        sa.Column("player_name", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("joined_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("game_id", "player_name", name="uq_players_game_name"),
        sa.UniqueConstraint("game_id", "role", name="uq_players_game_role"),
    )
    op.create_foreign_key(
        "fk_games_winner_player_id_players",
        "games",
        "players",
        ["winner_player_id"],
        ["id"],
    )
    op.create_table(
        "secrets",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("game_id", sa.Integer(), sa.ForeignKey("games.id"), nullable=False),
        sa.Column("player_id", sa.Integer(), sa.ForeignKey("players.id"), nullable=False, unique=True),
        sa.Column("secret_value", sa.String(), nullable=False),
        sa.Column("change_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("set_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "guesses",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("game_id", sa.Integer(), sa.ForeignKey("games.id"), nullable=False),
        sa.Column("player_id", sa.Integer(), sa.ForeignKey("players.id"), nullable=False),
        sa.Column("guess_value", sa.String(), nullable=False),
        sa.Column("a_count", sa.Integer(), nullable=False),
        sa.Column("b_count", sa.Integer(), nullable=False),
        sa.Column("is_win", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("guessed_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("guesses")
    op.drop_table("secrets")
    op.drop_constraint("fk_games_winner_player_id_players", "games", type_="foreignkey")
    op.drop_table("players")
    op.drop_table("games")
