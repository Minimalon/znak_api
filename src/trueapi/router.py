from base64 import b64encode
from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from src.trueapi.dependencies import doc_list, doc_info
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
        params: Dict[str, Any] = Depends(doc_list)
) -> dict:
    try:
        znak = Znak(token=token)
        docs = await znak.get_doc_list(params)
        return await docs.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/doc/{docId}/info', name='Информация о документе',
            description='Метод получения содержимого документа по идентификатору',
            )
async def doc_info(
        token: str,
        params: Dict[str, Any] = Depends(doc_info)
) -> list[dict]:
    znak = Znak(token=token)
    doc = await znak.get_doc_info(params['docId'])
    return await doc.json()
