from pydantic import BaseModel
from typing import List

class MailBodyModel(BaseModel):
    body: str
    to: List[str]
    subject: str
