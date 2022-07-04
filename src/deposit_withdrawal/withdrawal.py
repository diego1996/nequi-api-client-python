import json
import secrets
import requests
from dataclasses import dataclass
from datetime import datetime
from src.auth import auth_token
from src.app_config import config
from src.deposit_withdrawal.get_token_rsa import rsa_token
from src.utils.constants import NEQUI_STATUS_CODE_SUCCESS, CLIENT_ID, NEQUI_CHANNEL
from src.utils.responses import NequiResponse


@dataclass
class WithdrawalResponse:
    phoneNumber: str
    name: str
    value: str
    date: str
    trnId: str
    token: str


class WithdrawalAPI:
    _rest_endpoint: str

    def __init__(self):
        self._rest_endpoint = '/agents/v2/-services-cashoutservice-cashout'

    def _call(self, phone: str, code: str, value: str) -> WithdrawalResponse:
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
                        'ServiceName': 'CashOutServices',
                        'ServiceOperation': 'cashOut',
                        'ServiceRegion': 'C001',
                        'ServiceVersion': '1.0.0'
                    }
                },
                'RequestBody': {
                    'any': {
                        'cashOutRQ': {
                            'phoneNumber': phone,
                            'token': rsa_token.get_token(),
                            'code': code,
                            'value': value,
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
                    rs = WithdrawalResponse(
                        **data.ResponseMessage.ResponseBody.any['cashOutConsultRS']
                    )
                    print(
                        "Solicitud de retiro realizada correctamente: "
                        f"\nCelular: {rs.phoneNumber} "
                        f"\nNombre: {rs.name} "
                        f"\nValor: {rs.value} "
                        f"\nID de la transacción: {rs.trnId} "
                        f"\nFecha: {rs.date} "
                    )
                    return rs
                else:
                    raise Exception(f'Error, StatusCode: {status_code} - StatusDesc: {status_desc}')
            else:
                raise Exception('Unable to connect to Nequi, please check the information sent.')
        except Exception as e:
            raise e

    def withdrawal(self, phone: str, code: str, value: str) -> WithdrawalResponse | None:
        try:
            return self._call(phone, code, value)
        except Exception as e:
            print(f'Depositos y retiros -> Error realizando el retiro -> {e}')
            return None
