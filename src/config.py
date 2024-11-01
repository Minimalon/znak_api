from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

src_path = Path(__file__).parent
dir_path = src_path.parent

class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(dir_path, '.env'),
        env_file_encoding='utf-8',
        extra='ignore',
    )


class ZnakConfig(BaseConfig):
    model_config = SettingsConfigDict(
        env_prefix='znak_',
    )
    trueApi_url: str
    edoLite_url: str

    async def true_api_v3(self):
        return f'{self.trueApi_url}/api/v3/true-api'

    async def true_api_v4(self):
        return f'{self.trueApi_url}/api/v4/true-api'

class CertificateConfig(BaseConfig):
    model_config = SettingsConfigDict(
        env_prefix='cert_',
    )

    thumbprint: str
    pin: str

znak_config = ZnakConfig()
certificate_config = CertificateConfig()