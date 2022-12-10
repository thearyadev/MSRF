from pydantic import BaseModel, Field
from datetime import datetime


class MicrosoftAccount(BaseModel):
    email: str
    password: str
    points: int = Field(default=0)
    lastExecution: datetime | None = Field(default=None)
