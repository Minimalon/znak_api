from base64 import b64encode

from fastapi import APIRouter, Depends

from src.znak import Znak

router = APIRouter(
    prefix='/auth',
    tags=['Авторизация'],
)


@router.post('/token', name='Получение токена')
async def auth(inn: str) -> str:
    znak = Znak(inn)
    login_data = await znak.get_uuid_and_data()
    signing = await znak.cryproPro.signing_data(b64encode(login_data['data'].encode()).decode())
    sign_data = await znak.simple_signin(login_data['uuid'], signing, inn=inn)
    return sign_data['token']
