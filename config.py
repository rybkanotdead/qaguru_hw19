from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path
from dotenv import load_dotenv

class Config(BaseSettings):
    context: str = 'local_emulator'
    bstack_userName: str = ''
    bstack_accessKey: str = ''
    app: str
    platformVersion: str = ''
    deviceName: str = ''
    udid: str = ''
    remote_url: str = ''
    timeout: float = 10.0

    model_config = SettingsConfigDict(
        env_file=('.env', f'.env.{context}', '.env.credentials'),
        env_file_encoding='utf-8'
    )

def load_config():
    context = os.getenv('context', 'local_emulator')
    env_path = Path(f'.env.{context}')
    load_dotenv(dotenv_path=env_path)
    if context == 'bstack':
        load_dotenv(dotenv_path=Path('.env.credentials'), override=True)

    base_config = Config(_env_file=env_path)
    base_config.context = context
    return base_config

config = load_config()
