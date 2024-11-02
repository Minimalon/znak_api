from fastapi import APIRouter, Depends

from src.znak import Znak

router = APIRouter(
    prefix='/auth',
    tags=['Авторизация'],
)


@router.post('/token', tags="Получение токена")
async def auth(inn: str) -> str:
    znak = Znak(inn)
    return await znak.create_token()
