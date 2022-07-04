import json
import secrets
import requests
from datetime import datetime
from src.auth import auth_token
from src.app_config import config
from src.utils.constants import NEQUI_STATUS_CODE_SUCCESS, CLIENT_ID, NEQUI_CHANNEL, NEQUI_STATUS_DESC_SUCCESS
from src.utils.responses import NequiResponse


class ReverseTransactionAPI:
    _rest_endpoint: str

    def __init__(self):
        self._rest_endpoint = '/agents/v2/-services-reverseservices-reversetransaction'

    def _call(self, phone: str, code: str, value: str, message_id: str, transaction_type: str) -> str:
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
                        'ServiceName': 'ReverseServices',
                        'ServiceOperation': 'reverseTransaction',
                        'ServiceRegion': 'C001',
                        'ServiceVersion': '1.0.0'
                    }
                },
                'RequestBody': {
                    'any': {
                        'reversionRQ': {
                            'phoneNumber': phone,
                            'code': code,
                            'value': value,
                            'messageId': message_id,
                            'type': transaction_type,
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
                    print(
                        "Reversión de la transacción realizada correctamente: "
                        f"\nEstado: {status_desc} "
                    )
                    return status_desc
                else:
                    raise Exception(f'Error, StatusCode: {status_code} - StatusDesc: {status_desc}')
            else:
                raise Exception('Unable to connect to Nequi, please check the information sent.')
        except Exception as e:
            raise e

    def reverse_transaction(self, phone: str, code: str, value: str, message_id: str, transaction_type: str) -> bool:
        try:
            result = self._call(phone, code, value, message_id, transaction_type)
            return True if result == NEQUI_STATUS_DESC_SUCCESS else False
        except Exception as e:
            print(f'Depositos y retiros -> Error realizando la reversión de la transacción -> {e}')
            return False
