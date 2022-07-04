import requests
from src.app_config import config
from src.auth import auth_token


class RSATokenAPI:
    _rest_endpoint: str
    _token: str

    def __init__(self):
        self._rest_endpoint = '/agents/v2/-services-keysservice-getpublic'
        self._token = ''

    def _call(self):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': auth_token.get_token(),
            'x-api-key': config.api_key
        }
        endpoint = f'{config.api_base_path}{self._rest_endpoint}'
        try:
            response = requests.request('POST', url=endpoint, headers=headers)
            if response and response.status_code == 200 and response.text:
                self._token = response.text
            else:
                raise Exception(f'Error, StatusCode: {response.status_code}')
        except Exception as e:
            raise e

    def get_token(self) -> str:
        try:
            if not self._token:
                self._call()
            return self._token
        except Exception as e:
            print(f'Depositos y retiros -> Error obteniendo el token RSA -> {e}')
            return ''


rsa_token = RSATokenAPI()
