from pydantic import BaseModel

class ChatRequest(BaseModel):
    userchat: str
    session_id: str | None = None 