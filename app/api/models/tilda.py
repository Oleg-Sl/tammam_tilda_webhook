from pydantic import BaseModel


class TildaFormData(BaseModel):
    name: str
    phone: str
    calc: str
    tranid: str
    formid: str
