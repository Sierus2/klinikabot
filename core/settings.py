from dataclasses import dataclass
from environs import Env


@dataclass
class Bots:
    bot_token: str
    admin_id: str


@dataclass
class Db:
    user: str
    host: str
    password: str
    db: str


@dataclass
class Settings:
    bots: Bots
    db: Db


def get_settings(path: str):
    env = Env()
    env.read_env(path)
    return Settings(
        bots=Bots(
            bot_token=env.str('BOT_TOKEN'),
            admin_id=env.str('ADMIN_ID'),
        ),
        db=Db(
            user=env.str('DB_USER'),
            host=env.str('DB_HOST'),
            password=env.str('DB_PASSWORD'),
            db=env.str('DB_DATABASE'),
        )
    )


settings = get_settings('.env')

