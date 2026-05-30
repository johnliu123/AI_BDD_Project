from behave import given, then, when
from sqlalchemy import text

from tests.features.helpers.http_response import attach_http_transport


@when("玩家以遊戲 ID {遊戲ID} 和名稱 {玩家名稱} 進入遊戲")
def step_enter_game(context, 遊戲ID, 玩家名稱):
    response = context.api_client.post(
        "/api/games",
        json={"gameId": 遊戲ID, "playerName": 玩家名稱},
    )
    attach_http_transport(context, response)


@given("已存在遊戲 {遊戲ID} 且狀態為 {遊戲狀態}")
def step_existing_game(context, 遊戲ID, 遊戲狀態):
    result = context.db_session.execute(
        text(
            """
            INSERT INTO games (game_id, phase)
            VALUES (:game_id, :phase)
            RETURNING id
            """
        ),
        {"game_id": 遊戲ID, "phase": 遊戲狀態},
    )
    game_pk = result.scalar_one()
    context.ids[f"game:{遊戲ID}"] = game_pk
    context.db_session.flush()


@given("遊戲 {遊戲ID} 已有玩家 {玩家名稱} 擔任 {玩家角色}")
def step_game_has_player(context, 遊戲ID, 玩家名稱, 玩家角色):
    game_pk = context.ids.get(f"game:{遊戲ID}")
    if game_pk is None:
        game_pk = context.db_session.execute(
            text("SELECT id FROM games WHERE game_id = :game_id"),
            {"game_id": 遊戲ID},
        ).scalar_one()
        context.ids[f"game:{遊戲ID}"] = game_pk

    result = context.db_session.execute(
        text(
            """
            INSERT INTO players (game_id, player_name, role)
            VALUES (:game_pk, :player_name, :role)
            RETURNING id
            """
        ),
        {"game_pk": game_pk, "player_name": 玩家名稱, "role": 玩家角色},
    )
    player_pk = result.scalar_one()
    context.ids[f"player:{遊戲ID}:{玩家名稱}"] = player_pk
    context.ids[f"player:{遊戲ID}:{玩家角色}"] = player_pk
    context.db_session.flush()


@then("錯誤訊息應為 {錯誤訊息}")
def step_error_message_should_be_unquoted(context, 錯誤訊息):
    response = getattr(context, "last_response", None)
    assert response is not None, "No response captured"
    payload = response.json()
    actual = (
        payload.get("message")
        or payload.get("detail")
        or payload.get("error", {}).get("message")
    )
    assert actual == 錯誤訊息, f"Expected message {錯誤訊息!r}, got {actual!r}; body={payload}"


@then("回應遊戲狀態應為 {遊戲狀態}")
def step_response_phase_should_be(context, 遊戲狀態):
    response = getattr(context, "last_response", None)
    assert response is not None, "No response captured"
    payload = response.json()
    actual = payload.get("phase")
    assert actual == 遊戲狀態, f"Expected response phase {遊戲狀態!r}, got {actual!r}; body={payload}"


@then("進入遊戲回應角色應為 {玩家角色}")
def step_enter_game_role_should_be(context, 玩家角色):
    response = getattr(context, "last_response", None)
    assert response is not None, "No response captured"
    payload = response.json()
    actual = payload.get("role")
    assert actual == 玩家角色, f"Expected response role {玩家角色!r}, got {actual!r}; body={payload}"


@then("遊戲 {遊戲ID} 狀態應為 {遊戲狀態}")
def step_game_phase_should_be(context, 遊戲ID, 遊戲狀態):
    actual = context.db_session.execute(
        text("SELECT phase FROM games WHERE game_id = :game_id"),
        {"game_id": 遊戲ID},
    ).scalar_one_or_none()
    assert actual == 遊戲狀態, f"Expected game {遊戲ID} phase {遊戲狀態!r}, got {actual!r}"
