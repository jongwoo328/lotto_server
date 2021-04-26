from fastapi import APIRouter, HTTPException
from typing import List

from model import FullLotto
from db import session, Lotto

router = APIRouter(prefix='/api/v1')

@router.get('/lotto', response_model=List[FullLotto])
async def get_full_lotto():
    lottos = session.query(Lotto).all()
    return lottos

@router.get('/lotto/{round}', response_model=FullLotto)
async def get_lotto_by_round(round):
    lotto = session.query(Lotto).filter(Lotto.round==round)
    if not lotto.count():
        raise HTTPException(status_code=404)
    return session.query(Lotto).filter(Lotto.round==round)[0]