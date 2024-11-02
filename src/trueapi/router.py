from base64 import b64encode

from fastapi import APIRouter, Depends

from src.znak import Znak

router = APIRouter(
    prefix='/trueapi',
    tags=['TrueApi'],
)


@router.post('/doc/list', name='Список всех документов',
             description='Метод получения списка загруженных документов в ГИС МТ')
async def doc_list(
        token: str,
        pg: str,
        dateFrom: str = None,
        dateTo: str = None,
        documentFormat: str = None,
        limit: int = 1000,
        number: str = None,
        order: str = "DESC",
        pageDir: str = "NEXT",
        senderInn: str = None,
        receiverInn: str = None,

) -> dict:
    znak = Znak(token=token)
    docs = await znak.get_doc_list({
        "pg": pg,
        "dateFrom": dateFrom,
        "dateTo": dateTo,
        "documentFormat": documentFormat,
        "limit": limit,
        "number": number,
        "order": order,
        "pageDir": pageDir,
        "senderInn": senderInn,
        "receiverInn": receiverInn
    })

    return await docs.json()
