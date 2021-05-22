import datetime
from typing import Optional

from pydantic import BaseModel


class FullLotto(BaseModel):
    round: int
    date: datetime.date
    first_count: int
    first_price: int
    second_count: int
    second_price: int
    third_count: int
    third_price: int
    fourth_count: int
    fourth_price: int
    fifth_count: int
    fifth_price: int
    num1: int
    num2: int
    num3: int
    num4: int
    num5: int
    num6: int
    bonus: int

    class Config:
        orm_mode = True
