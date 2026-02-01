from typing import Optional
from pydantic import BaseModel


class WebhookResponse(BaseModel):
    status: str
    message: Optional[str] = None
