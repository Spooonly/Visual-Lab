from pydantic import BaseModel
from typing import List

class MixRequest(BaseModel):
    reagents: List[str]