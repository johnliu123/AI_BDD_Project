from pydantic import BaseModel


class EnterGameResponse(BaseModel):
    gameId: str
    playerId: str
    role: str
    phase: str
    message: str | None = None


class SetSecretResponse(BaseModel):
    gameId: str
    phase: str


class ErrorResponse(BaseModel):
    message: str
    code: str
