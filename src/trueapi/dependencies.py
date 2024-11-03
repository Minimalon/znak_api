from typing import Any, Dict

from fastapi import Depends
from fastapi.params import Query


def doc_list(
        pg: str,
        dateFrom: str = None,
        dateTo: str = None,
        documentFormat: str = None,
        limit: int = 100,
        number: str = None,
        order: str = "DESC",
        pageDir: str = "NEXT",
        senderInn: str = None,
        receiverInn: str = None
) -> Dict[str, Any]:
    params = {
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
    }
    # Удаляем параметры со значением None
    filtered_params = {k: v for k, v in params.items() if v is not None}
    return filtered_params


async def doc_info(
        docId: str,
        body: bool = Query(
            False,
            description='Признак необходимости в теле ответа содержимого документа\n'
                        '«true» — содержимое отправленного документа возвращается в ответе метода;\n'
                        '«false» — содержимое отправленного документа не возвращается в ответе метода',
        ),
        content: bool = Query(
            False,
            description='Признак необходимости контента документа в теле ответа \n'
                        '«true» — контент документа возвращается в ответе метода;\n'
                        '«false» — контент документа не возвращается в ответе метода',
        ),
        pg: str = Query(None, description='Товарная группа'),
        limit: int = Query(36000, description='Количество кодовв теле документа'),
        pageNumber: int = Query(1, description='Лимит вывода информации по кодам')
) -> Dict[str, Any]:
    params = {
        "docId": docId,
        "body": body,
        "content": content,
        "pg": pg,
        "limit": limit,
        "pageNumber": pageNumber
    }
    # Удаляем параметры со значением None
    filtered_params = {k: v for k, v in params.items() if v is not None}
    return filtered_params
