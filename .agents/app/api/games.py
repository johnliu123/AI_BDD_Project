from typing import Any

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.repositories.game_repository import GameRepository
from app.services.enter_game_service import EnterGameError, EnterGameService
from app.services.set_secret_service import SetSecretError, SetSecretService

router = APIRouter(prefix="/games", tags=["Games"])


@router.post("")
def enter_game(payload: dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    service = EnterGameService(GameRepository(db))
    try:
        result = service.enter_game(
            game_id=payload.get("gameId"),
            player_name=payload.get("playerName"),
        )
    except EnterGameError as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.message, "code": exc.code},
        )
    return result


@router.post("/{game_id}/secrets")
def set_secret(game_id: str, payload: dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    service = SetSecretService(GameRepository(db))
    try:
        result = service.set_secret(
            game_id=game_id,
            player_id=payload.get("playerId"),
            secret=payload.get("secret"),
        )
    except SetSecretError as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.message, "code": exc.code},
        )
    return result
