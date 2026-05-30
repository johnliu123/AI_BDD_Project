from behave import given, then, when
from sqlalchemy import text

from tests.features.helpers.http_response import attach_http_transport
from tests.features.steps.雙人猜數字對戰.secret_steps import _resolve_player_pk


@given("玩家 {玩家ID} 在遊戲 {遊戲ID} 已修改秘密數字 {修改次數:d} 次")
def step_player_secret_change_count(context, 玩家ID, 遊戲ID, 修改次數):
    player_pk = _resolve_player_pk(context, 遊戲ID, 玩家ID)
    context.db_session.execute(
        text(
            """
            UPDATE secrets
            SET change_count = :change_count
            WHERE player_id = :player_pk
            """
        ),
        {"change_count": 修改次數, "player_pk": player_pk},
    )
    context.db_session.flush()


@when("玩家 {玩家ID} 在遊戲 {遊戲ID} 修改秘密數字為 {秘密數字}")
def step_change_secret(context, 玩家ID, 遊戲ID, 秘密數字):
    player_pk = _resolve_player_pk(context, 遊戲ID, 玩家ID)
    response = context.api_client.patch(
        f"/api/games/{遊戲ID}/secrets/{player_pk}",
        json={"secret": 秘密數字},
    )
    attach_http_transport(context, response)


@then("玩家 {玩家ID} 在遊戲 {遊戲ID} 的秘密數字應為 {秘密數字}")
def step_player_secret_should_be(context, 玩家ID, 遊戲ID, 秘密數字):
    player_pk = _resolve_player_pk(context, 遊戲ID, 玩家ID)
    actual = context.db_session.execute(
        text("SELECT secret_value FROM secrets WHERE player_id = :player_pk"),
        {"player_pk": player_pk},
    ).scalar_one_or_none()
    assert actual == 秘密數字, f"Expected player {玩家ID} secret {秘密數字!r}, got {actual!r}"


@then("玩家 {玩家ID} 的秘密數字修改次數應為 {修改次數:d}")
def step_player_secret_change_count_should_be(context, 玩家ID, 修改次數):
    matching_keys = [key for key in context.ids if key.startswith("player:") and key.endswith(f":{玩家ID.upper()}")]
    assert matching_keys, f"Cannot resolve player {玩家ID!r} from scenario ids"
    player_pk = context.ids[matching_keys[0]]
    actual = context.db_session.execute(
        text("SELECT change_count FROM secrets WHERE player_id = :player_pk"),
        {"player_pk": player_pk},
    ).scalar_one_or_none()
    assert actual == 修改次數, f"Expected player {玩家ID} change_count {修改次數!r}, got {actual!r}"
