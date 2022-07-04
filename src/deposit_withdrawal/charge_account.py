import json
import secrets
import requests
from dataclasses import dataclass
from datetime import datetime
from src.auth import auth_token
from src.app_config import config
from src.utils.constants import NEQUI_STATUS_CODE_SUCCESS, CLIENT_ID, NEQUI_CHANNEL
from src.utils.responses import NequiResponse


@dataclass
class ChargeAccountResponse:
    trnId: str
    date: str
    name: str


class ChargeAccountAPI:
    _rest_endpoint: str

    def __init__(self):
        self._rest_endpoint = '/agents/v2/-services-cashinservice-cashin'

    def _call(self, phone: str, code: str, value: float) -> ChargeAccountResponse:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': auth_token.get_token(),
            'x-api-key': config.api_key
        }
        data = {
            'RequestMessage': {
                'RequestHeader': {
                    'Channel': NEQUI_CHANNEL,
                    'RequestDate': datetime.now().strftime('%Y-%m-%dT%H:%M:%S0Z'),
                    'MessageID': secrets.token_hex(5),
                    'ClientID': CLIENT_ID,
                    'Destination': {
                        'ServiceName': 'CashInService',
                        'ServiceOperation': 'cashIn',
                        'ServiceRegion': 'C001',
                        'ServiceVersion': '1.0.0'
                    }
                },
                'RequestBody': {
                    'any': {
                        'cashInRQ': {
                            'phoneNumber': phone,
                            'code': code,
                            'value': str(value)
                        }
                    }
                }
            }
        }
        endpoint = f'{config.api_base_path}{self._rest_endpoint}'
        try:
            response = requests.request('POST', url=endpoint, data=json.dumps(data), headers=headers)
            if response and response.status_code == 200 and response.json():
                data = NequiResponse(**response.json())
                status_code = data.ResponseMessage.ResponseHeader.Status.StatusCode
                status_desc = data.ResponseMessage.ResponseHeader.Status.StatusDesc
                if status_code == NEQUI_STATUS_CODE_SUCCESS:
                    rs = ChargeAccountResponse(**data.ResponseMessage.ResponseBody.get('cashInFinacleRS', {}))
                    print(
                        "Recarga realizada correctamente: "
                        f"\nID de la transacción: {rs.trnId} "
                        f"\nFecha de la transacción: {rs.date} "
                        f"\nNombre: {rs.name}"
                    )
                    return rs
                else:
                    raise Exception(f'Error, StatusCode: {status_code} - StatusDesc: {status_desc}')
            else:
                raise Exception('Unable to connect to Nequi, please check the information sent.')
        except Exception as e:
            raise e

    def charge_account(self, phone: str, code: str, value: float) -> ChargeAccountResponse | None:
        try:
            return self._call(phone, code, value)
        except Exception as e:
            print(f'Depositos y retiros -> Error recargando la cuenta -> {e}')
            return None
