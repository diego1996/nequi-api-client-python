import json
import secrets
import requests
from dataclasses import dataclass
from datetime import datetime
from src.auth import auth_token
from src.app_config import config
from src.utils import constants
from src.utils.responses import NequiResponse


@dataclass
class CheckWithdrawalResponse:
    phoneNumber: str
    value: str
    description: str
    reference: str


class CheckWithdrawalAPI:
    _rest_endpoint: str

    def __init__(self):
        self._rest_endpoint = '/agents/v2/-services-cashoutservice-cashoutconsult'

    def _call(self, phone: str) -> CheckWithdrawalResponse:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': auth_token.get_token(),
            'x-api-key': config.api_key
        }
        data = {
            'RequestMessage': {
                'RequestHeader': {
                    'Channel': constants.NEQUI_CHANNEL_DEPOSIT_WITHDRAWALS,
                    'RequestDate': datetime.now().strftime('%Y-%m-%dT%H:%M:%S0Z'),
                    'MessageID': secrets.token_hex(5),
                    'ClientID': constants.CLIENT_ID,
                    'Destination': {
                        'ServiceName': 'CashOutServices',
                        'ServiceOperation': 'cashOutConsult',
                        'ServiceRegion': 'C001',
                        'ServiceVersion': '1.0.0'
                    }
                },
                'RequestBody': {
                    'any': {
                        'cashOutConsultRQ': {
                            'phoneNumber': phone
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
                if status_code == constants.NEQUI_STATUS_CODE_SUCCESS:
                    rs = CheckWithdrawalResponse(
                        **data.ResponseMessage.ResponseBody.any['cashOutConsultRS']
                    )
                    print(
                        "Solicitud de retiro validada correctamente: "
                        f"\nCelular: {rs.phoneNumber} "
                        f"\nValor: {rs.value} "
                        f"\nDescripción: {rs.description} "
                        f"\nReferencia: {rs.reference} "
                    )
                    return rs
                else:
                    raise Exception(f'Error, StatusCode: {status_code} - StatusDesc: {status_desc}')
            else:
                raise Exception('Unable to connect to Nequi, please check the information sent.')
        except Exception as e:
            raise e

    def check_withdrawal(self, phone: str) -> CheckWithdrawalResponse | None:
        try:
            return self._call(phone)
        except Exception as e:
            print(f'Depositos y retiros -> Error validando solicitud de retiro -> {e}')
            return None
