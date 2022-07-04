import base64
import requests
from datetime import datetime, timedelta
from app_config import config
from dataclasses import dataclass


@dataclass
class _TokenResponse:
    access_token: str
    token_type: str
    expires_in: int


class AuthAPI:
    _token: str
    _token_type: str
    _expires_at: datetime | None

    def __init__(self):
        self._token = ''
        self._token_type = ''
        self._expires_at = None

    def _auth(self):
        token_encoded = base64.b64encode(f'{config.client_id}:{config.client_secret}'.encode()).decode()
        authorization = f'Basic {token_encoded}'
        headers = {
            'Authorization': authorization,
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        params = {
            'grant_type': config.auth_grant_type
        }
        try:
            response = requests.request('POST', url=config.auth_uri, params=params, headers=headers)
            if response and response.status_code == 200 and response.json():
                data = _TokenResponse(**response.json())
                self._token = data.access_token
                self._token_type = data.token_type
                self._expires_at = datetime.now() + timedelta(seconds=data.expires_in)
            else:
                raise Exception('Unable to connect to Nequi, please check the information sent.')
        except Exception as e:
            raise e

    def _is_valid_token(self) -> bool:
        if not self._expires_at:
            return False

        return datetime.now() < self._expires_at

    def get_token(self, full: bool = True) -> str:
        if not self._is_valid_token():
            self._auth()

        return f'{self._token_type} {self._token}' if full else self._token


auth_token = AuthAPI()
