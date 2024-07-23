import os
from dotenv import load_dotenv

# load 
load_dotenv(override=True)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'faut pas tu vas me fé hein'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = os.getenv('DB_URL')
    DB_SCHEMA = os.getenv('DB_SCHEMA_LOCAL')

class ProductionConfig(Config):
    DATABASE_URI = os.getenv('DB_NEON_URL')
    DB_SCHEMA = os.getenv('DB_SCHEMA_NEON')

config = {
    'development' : DevelopmentConfig,
    'production' : ProductionConfig,

    'default' : DevelopmentConfig
}

if __name__ == "__main__" :
    load_dotenv(override=True)
    app_config = config['development'] 
    db_url = app_config.DATABASE_URI
    db_schema = app_config.DB_SCHEMA

    print("DB URL : ", db_url)
    print("DB SCHEMA : ", db_schema)