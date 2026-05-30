from behave import given, when
from sqlalchemy import text

from tests.features.helpers.http_response import attach_http_transport


def _resolve_player_pk(context, game_id: str, player_id: str) -> int:
    role_or_id = player_id.upper() if player_id.lower() in {"p1", "p2"} else player_id
    stored = context.ids.get(f"player:{game_id}:{role_or_id}")
    if stored is not None:
        return stored
    if str(player_id).isdigit():
        return int(player_id)
    raise AssertionError(f"Cannot resolve player {player_id!r} in game {game_id!r}")


def _resolve_game_pk(context, game_id: str) -> int:
    stored = context.ids.get(f"game:{game_id}")
    if stored is not None:
        return stored
    game_pk = context.db_session.execute(
        text("SELECT id FROM games WHERE game_id = :game_id"),
        {"game_id": game_id},
    ).scalar_one()
    context.ids[f"game:{game_id}"] = game_pk
    return game_pk


@when("玩家 {玩家ID} 在遊戲 {遊戲ID} 設定秘密數字 {秘密數字}")
def step_set_secret(context, 玩家ID, 遊戲ID, 秘密數字):
    player_pk = _resolve_player_pk(context, 遊戲ID, 玩家ID)
    response = context.api_client.post(
        f"/api/games/{遊戲ID}/secrets",
        json={"playerId": str(player_pk), "secret": 秘密數字},
    )
    attach_http_transport(context, response)


@given("玩家 {玩家ID} 在遊戲 {遊戲ID} 已設定秘密數字 {秘密數字}")
def step_player_has_secret(context, 玩家ID, 遊戲ID, 秘密數字):
    game_pk = _resolve_game_pk(context, 遊戲ID)
    player_pk = _resolve_player_pk(context, 遊戲ID, 玩家ID)
    secret_pk = context.db_session.execute(
        text(
            """
            INSERT INTO secrets (game_id, player_id, secret_value, change_count)
            VALUES (:game_pk, :player_pk, :secret_value, 0)
            RETURNING id
            """
        ),
        {"game_pk": game_pk, "player_pk": player_pk, "secret_value": 秘密數字},
    ).scalar_one()
    context.ids[f"secret:{遊戲ID}:{玩家ID.upper()}"] = secret_pk
    context.db_session.flush()
