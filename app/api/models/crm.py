from typing import List
from pydantic import BaseModel


class Phone(BaseModel):
    value: str
    value_type: str = "WORK"


class LeadCreationFields(BaseModel):
    title: str
    name: str
    phone: List[Phone]
    modules_data: str
    opportunity: str
