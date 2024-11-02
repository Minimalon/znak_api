from base64 import b64encode
from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends

from src.trueapi.dependencies import get_filtered_params
from src.znak import Znak

router = APIRouter(
    prefix='/trueapi',
    tags=['TrueApi'],
)


@router.post('/doc/list', name='Список всех документов',
             description='Метод получения списка загруженных документов в ГИС МТ',
             )
async def doc_list(
        token: str,
        params: Dict[str, Any] = Depends(get_filtered_params)
) -> dict:
    znak = Znak(token=token)
    docs = await znak.get_doc_list(params)
    return await docs.json()
