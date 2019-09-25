# Logging Config
LOG_PATH = '/var/log/flask-postgres'
LOGFILE = f'{LOG_PATH}/flask-postgres.log'
LOGLEVEL = 'DEBUG'

# API Config
API_IP = '0.0.0.0'
API_PORT = 1212

# DB Config
DB_USER = 'postgres'
DB_PASSWD = 'postgres'
DB_HOST = 'localhost'
DB_NAME = 'flask_postgres'
DB_CONNECTION_STRING = (
    f'postgresql+psycopg2://{DB_USER}:{DB_PASSWD}@{DB_HOST}/{DB_NAME}'
)