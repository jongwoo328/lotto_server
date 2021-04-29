import datetime

from fastapi import APIRouter, HTTPException
from typing import List

from model import FullLotto
from db import session_scope, Lotto


router = APIRouter(prefix='/api/v1')

@router.get('/lottos', response_model=List[FullLotto])
async def lottos():
    with session_scope as session:
        lottos = session.query(Lotto).all()
        return lottos

@router.get('/lottos/last', response_model=FullLotto)
async def last_lotto():
    with session_scope as session:
        lotto = session.query(Lotto).order_by(Lotto.round.desc()).first()
        return lotto

@router.get('/lottos/{round}', response_model=FullLotto)
async def get_lotto_by_round(round):
    with session_scope as session:
        lotto = session.query(Lotto).filter(Lotto.round==round)
        if not lotto.count():
            raise HTTPException(status_code=404, detail='존재하지 않는 회차입니다.')
        return lotto[0]