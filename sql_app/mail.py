from typing import List

from pydantic import BaseModel


class MailBodyModel(BaseModel):
    body: str
    to: List[str]
    subject: str
