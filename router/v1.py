import datetime
import random
from typing import List, Optional, Tuple

from fastapi import APIRouter, HTTPException, Query, Response, status
from sqlalchemy import and_
from sqlalchemy.sql import exists, column

from model import FullLotto
from db import session_scope, Lotto
from .util.util import get_numbers, check_second_and_third
from .util.scrap import get_round, get_new_data


router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.get("/lottos/update", response_model=FullLotto, status_code=200)
async def update_new_data(response: Response):
    with session_scope() as session:
        last = session.query(Lotto)[-1]
        scrapped_round = get_round()
        if last.round != scrapped_round:
            new_data = get_new_data()
            session.add(Lotto(**new_data))
            session.commit()
            response.status_code = status.HTTP_201_CREATED
            return new_data
        return last


@router.get("/lottos/new")
async def get_new_lotto(
    q: List[str] = Query([]),
    count: str = Query("1", max_length=1, min_length=1, regex="^(1|5)$"),
):
    result = []
    for _ in range(int(count)):
        with session_scope() as session:
            while True:
                numbers = random.sample(range(1, 46), 6)
                numbers.sort()
                num1, num2, num3, num4, num5, num6 = numbers
                if "except_first" in q:
                    conditions = {
                        "num1": num1,
                        "num2": num2,
                        "num3": num3,
                        "num4": num4,
                        "num5": num5,
                        "num6": num6,
                    }
                    filters = [
                        column(key) == value for key, value in conditions.items()
                    ]
                    exist = session.query(exists(Lotto).where(and_(*filters))).scalar()
                    if exist:
                        continue
                if "except_second" in q or "except_third" in q:
                    lottos = session.query(
                        Lotto.num1,
                        Lotto.num2,
                        Lotto.num3,
                        Lotto.num4,
                        Lotto.num5,
                        Lotto.num6,
                        Lotto.bonus,
                    ).all()
                    has_won = check_second_and_third(lottos=lottos, picked=numbers, q=q)
                    if has_won:
                        continue
                break
            result.append(numbers)
    return result


@router.get("/lottos", response_model=List[FullLotto])
async def lottos():
    with session_scope() as session:
        lottos = session.query(Lotto).all()
        return lottos


@router.get("/lottos/last", response_model=FullLotto)
async def last_lotto():
    with session_scope() as session:
        lotto = session.query(Lotto)[-1]
        return lotto


@router.get("/lottos/{round}", response_model=FullLotto)
async def get_lotto_by_round(round):
    with session_scope() as session:
        lotto = session.query(Lotto).filter(Lotto.round == round)
        if not lotto.count():
            raise HTTPException(status_code=404, detail="???????????? ?????? ???????????????.")
        return lotto[0]
