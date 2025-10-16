import os
from dotenv import load_dotenv

env_file_path = os.environ.get("ENV_FILE_PATH")
if env_file_path and os.path.exists(env_file_path):
    load_dotenv(env_file_path)

class Config:
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    if not all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT]):
        raise Exception("Variáveis de ambiente do banco não estão todas definidas.")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

config = Config()
