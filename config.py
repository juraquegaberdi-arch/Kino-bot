import json
from typing import Any, List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str = '8955497555:AAFX6IqsriuDmB8zkBoI3QnEUVNlUmczbHM'
    DATABASE_URL: str
    DEBUG: bool = False
    ADMINS: Any = [7327126896]
    SUBSCRIPTION_CHANNELS: Any = []

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @staticmethod
    def _parse_int_list(value: Any) -> List[int]:
        if value is None or value == "":
            return []
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return []
            if value.startswith("[") and value.endswith("]"):
                value = json.loads(value)
            else:
                value = value.split(",")
        return [int(item) for item in value]

    def model_post_init(self, __context: Any) -> None:
        self.ADMINS = self._parse_int_list(self.ADMINS)
        self.SUBSCRIPTION_CHANNELS = self._parse_int_list(self.SUBSCRIPTION_CHANNELS)


settings = Settings()
