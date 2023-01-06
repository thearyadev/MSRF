from datetime import datetime

from pydantic import BaseModel, Field


class MicrosoftAccount(BaseModel):
    id: str | None = Field(default=None)
    email: str
    password: str
    points: int = Field(default=0)
    lastExec: datetime | None = Field(default=None)