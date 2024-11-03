from typing import Any, Dict

from fastapi.params import Query
def depen_auth(
        inn: str = Query(
            '160502035960',
            description='ИНН участника у которого оформлена доверенность на config.main_thumbprint',
        )
) -> Dict[str, Any]:
    return {'inn': inn}
