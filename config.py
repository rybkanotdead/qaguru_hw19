from pydantic_settings import BaseSettings


class Config(BaseSettings):
    bstack_userName: str
    bstack_accessKey: str
    app: str

config = Config(_env_file=".env")