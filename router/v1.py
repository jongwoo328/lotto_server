import datetime
import random

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from sqlalchemy import and_
from sqlalchemy.sql import exists, column

from model import FullLotto
from db import session_scope, Lotto
from .util.util import get_numbers, check_second_and_third


router = APIRouter(prefix='/api/v1')

@router.get('/lottos/new')
async def get_new_lotto(q: List[str] = Query([])):
    with session_scope() as session:
        while True:
            numbers = random.sample(range(1, 46), 6)
            numbers.sort()
            num1, num2, num3, num4, num5, num6 = numbers
            if 'except_first' in q:
                conditions = {
                    'num1': num1,
                    'num2': num2,
                    'num3': num3,
                    'num4': num4,
                    'num5': num5,
                    'num6': num6
                }
                filters = [column(key) == value for key, value in conditions.items()]
                exist = session.query(exists(Lotto).where(and_(*filters))).scalar()
                if exist:
                    continue
            if 'except_second' in q or 'except_third' in q:
                lottos = session.query(
                    Lotto.num1,
                    Lotto.num2,
                    Lotto.num3,
                    Lotto.num4,
                    Lotto.num5,
                    Lotto.num6,
                    Lotto.bonus
                ).all()
                has_won = check_second_and_third(lottos=lottos, picked=numbers, q=q)
                if has_won:
                    continue
            break
    return numbers

@router.get('/lottos', response_model=List[FullLotto])
async def lottos():
    with session_scope() as session:
        lottos = session.query(Lotto).all()
        return lottos

@router.get('/lottos/last', response_model=FullLotto)
async def last_lotto():
    with session_scope() as session:
        lotto = session.query(Lotto).order_by(Lotto.round.desc()).first()
        return lotto

@router.get('/lottos/{round}', response_model=FullLotto)
async def get_lotto_by_round(round):
    with session_scope() as session:
        lotto = session.query(Lotto).filter(Lotto.round==round)
        if not lotto.count():
            raise HTTPException(status_code=404, detail='존재하지 않는 회차입니다.')
        return lotto[0]
