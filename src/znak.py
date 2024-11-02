import json
from fastapi.exceptions import HTTPException

from aiohttp import ClientResponse, ClientSession

from src.config import znak_config
from src.loggers import znak_log
from src.cryptopro import CryproPro

from base64 import b64encode


class Znak:
    def __init__(self, inn_to_auth: str = None, token: str = None):
        """
        :param inn_to_auth: ИНН пользователя к которому нужно аутентифицироваться
        """
        self.token = token
        self.cryproPro = CryproPro()
        self.inn_to_auth = inn_to_auth

    @staticmethod
    async def log_request(method: str, url: str, headers: dict = None, data: str = None) -> None:
        log = znak_log.bind(url=url, headers=headers, data=data)
        log.info(f"{method} {url}")

    @staticmethod
    async def log_response(response: ClientResponse) -> None:
        log = znak_log.bind(status_code=response.status, url=response.url)
        log.info(str(response.url))
        if response.ok:
            log.success(await response.text())
        else:
            log.error(await response.text())

    async def _get(self, url: str, params: dict = None, headers: dict = None, data: str = None) -> ClientResponse:
        if self.token is not None:
            headers = {"Authorization": f"Bearer {self.token}"} if headers is None else {
                "Authorization": f"Bearer {self.token}", **headers}
        async with ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as resp:
                await self.log_request('GET', str(resp.url), headers=headers, data=data)
                await self.log_response(resp)
                if not resp.ok:
                    raise HTTPException(status_code=resp.status, detail=await resp.json())
                return resp

    async def _post(self, url: str, params: dict = None, headers: dict = None, data: str = None) -> ClientResponse:
        if self.token is not None:
            headers = {"Authorization": f"Bearer {self.token}"} if headers is None else {
                "Authorization": f"Bearer {self.token}", **headers}
        async with ClientSession() as session:
            async with session.post(url, params=params, headers=headers, data=data) as resp:
                await self.log_request('POST', str(resp.url), headers=headers, data=data)
                await self.log_response(resp)
                if not resp.ok:
                    raise HTTPException(status_code=resp.status, detail=await resp.json())
                return resp

    async def _put(self, url: str, params: dict = None, headers: dict = None, data: str = None) -> ClientResponse:
        if self.token is not None:
            headers = {"Authorization": f"Bearer {self.token}"} if headers is None else {
                "Authorization": f"Bearer {self.token}", **headers}
        async with ClientSession() as session:
            async with session.put(url, params=params, headers=headers, data=data) as resp:
                await self.log_request('PUT', str(resp.url), headers=headers, data=data)
                await self.log_response(resp)
                if not resp.ok:
                    raise HTTPException(status_code=resp.status, detail=await resp.json())
                return resp

    # region Login
    async def simple_signin(self, uuid: str, signing: str, inn: str) -> dict:
        """
        Логинимся в ЧЗ
        :param inn: ИНН участника у которого оформлена доверенность на config.main_thumbprint
        :param uuid:
        :param signing: Подписанная data
        :return: Токен авторизации
        """
        headers = {'Content-Type': 'application/json', "accept": "application/json"}
        data = {'uuid': uuid, "data": signing} if inn is None else {'uuid': uuid, "data": signing, 'inn': inn}
        url = f'{await znak_config.true_api_v3()}/auth/simpleSignIn'
        response = await self._post(url, headers=headers, data=json.dumps(data))
        return await response.json()

    async def create_token(self) -> str:
        """Создание токена"""
        login_data = await self.get_uuid_and_data()
        signing = await self.cryproPro.signing_data(b64encode(login_data['data'].encode()).decode())
        sign_data = await self.simple_signin(login_data['uuid'], signing, self.inn_to_auth)
        znak_log.info(sign_data)
        return sign_data['token']

    async def get_uuid_and_data(self) -> dict:
        """Начало авторизации. Получение uuid и data"""
        headers = {"accept": "application/json"}
        url = f'{await znak_config.true_api_v3()}/auth/key'
        response = await self._get(url, headers=headers)
        return await response.json()

    # endregion

    async def get_doc_list(self, args) -> ClientResponse:
        """
        Список всех документов (Метод получения списка загруженных документов в ГИС МТ)
        :param args: urlencode. Обязательный памераметр pg
        :return: Список документов
        """
        return await self._get(
            url=f'{await znak_config.true_api_v4()}/doc/list',
            params=args,
        )

