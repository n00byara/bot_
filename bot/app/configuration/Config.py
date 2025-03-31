import os
from dotenv import load_dotenv

from configuration.СhangeError import СhangeError

load_dotenv()

class Config:
    class _Postgres:
        username: str = None
        userpassword: str = None
        database: str = None
        host: str = None
        port: str = None

        def __init__(self):
            self._username = os.getenv("POSTGRES_USER")
            self._database = os.getenv("POSTGRES_DB")
            self._userpassword = os.getenv("POSTGRES_PASSWORD")
            self._host = os.getenv("POSTGRES_HOST")
            self._port = os.getenv("POSTGRES_PORT")

        @property
        def username(self):
            return self._username
        
        @username.setter
        def username(self, value):
            raise СhangeError()
        
        @property
        def database(self):
            return self._database
        
        @database.setter
        def database(self, value):
            raise СhangeError()

        @property
        def userpassword(self):
            return self._userpassword
        
        @userpassword.setter
        def userpassword(self, value):
            raise СhangeError()
        
        @property
        def host(self):
            return self._host
        
        @host.setter
        def host(self, value):
            raise СhangeError()
        
        @property
        def port(self):
            return self._port
        
        @port.setter
        def port(self, value):
            raise СhangeError()
        
    token: str = None
    postgres: _Postgres = None

    def __init__(self):
        self._token = os.getenv("TOKEN")
        self._postgres = self._Postgres()
    
    @property
    def token(self):
        return self._token
    
    @token.setter
    def token(self, value):
        raise СhangeError()
    
    @property
    def postgres(self):
        return self._postgres
    
    @postgres.setter
    def postgres(self, value):
        raise СhangeError()