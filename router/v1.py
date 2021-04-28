import datetime

from fastapi import APIRouter, HTTPException
from typing import List

from model import FullLotto
from db import session, Lotto


router = APIRouter(prefix='/api/v1')

@router.get('/lottos', response_model=List[FullLotto])
async def lottos():
    lottos = session.query(Lotto).all()
    session.close()
    return lottos

@router.get('/lottos/last', response_model=FullLotto)
async def last_lotto():
    lotto = session.query(Lotto).order_by(Lotto.round.desc()).first()
    return lotto

@router.get('/lottos/{round}', response_model=FullLotto)
async def get_lotto_by_round(round):
    lotto = session.query(Lotto).filter(Lotto.round==round)[0]
    if not lotto.count():
        raise HTTPException(status_code=404, detail='존재하지 않는 회차입니다.')
    session.close()
    return lotto