from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime


class MixRequest(BaseModel):
    reagents: List[str]


class ExperimentOut(BaseModel):
    id: int
    created_at: datetime
    reagents: List[str]
    result: Dict[str, Any]


class NotebookOut(BaseModel):
    items: List[ExperimentOut]
