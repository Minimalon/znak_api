from fastapi import APIRouter, Depends

from src.znak import Znak

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/token')
async def auth(inn: str) -> str:
    znak = Znak(inn)
    return await znak.create_token()
