from pydantic import BaseModel


# Модель для валидации входящих данных
class Message(BaseModel):
    action: str
    connected: bool
    detail: str
    status: int
