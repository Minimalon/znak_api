from typing import Any, Dict


def get_filtered_params(
        pg: str,
        dateFrom: str = None,
        dateTo: str = None,
        documentFormat: str = None,
        limit: int = 1000,
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