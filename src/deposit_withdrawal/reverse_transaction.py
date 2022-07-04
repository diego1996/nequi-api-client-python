import json
import secrets
import requests
from datetime import datetime
from src.auth import auth_token
from src.app_config import config
from src.utils import constants
from src.utils.responses import NequiResponse


class ReverseTransactionAPI:
    _status_code: str
    _status_desc: str
    _rest_endpoint: str

    def __init__(self):
        self._rest_endpoint = '/agents/v2/-services-reverseservices-reversetransaction'

    def _call(self, phone: str, code: str, value: str, message_id: str, transaction_type: str) -> None:
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
                if status_code == constants.NEQUI_STATUS_CODE_SUCCESS:
                    print(
                        "Reversión de la transacción realizada correctamente: "
                        f"\nEstado: {status_desc} "
                    )
                    self._status_code = status_code
                    self._status_desc = status_desc
                else:
                    raise Exception(f'Error, StatusCode: {status_code} - StatusDesc: {status_desc}')
            else:
                raise Exception('Unable to connect to Nequi, please check the information sent.')
        except Exception as e:
            raise e

    def _reverse_transaction(self, phone: str, code: str, value: str, message_id: str, transaction_type: str) -> None:
        try:
            self._call(phone, code, value, message_id, transaction_type)
        except Exception as e:
            print(f'Depositos y retiros -> Error realizando la reversión de la transacción -> {e}')

    def reverse_deposit(self, phone: str, code: str, value: str, message_id: str) -> None:
        transaction_type = 'cashin'
        self._reverse_transaction(phone, code, value, message_id, transaction_type)

    def reverse_withdrawal(self, phone: str, code: str, value: str, message_id: str) -> None:
        transaction_type = 'cashout'
        self._reverse_transaction(phone, code, value, message_id, transaction_type)

    def is_reversed(self) -> bool:
        return True if self._status_code == constants.NEQUI_STATUS_CODE_SUCCESS else False

    def get_status_code(self) -> str:
        return self._status_code

    def get_status_desc(self) -> str:
        return self._status_desc
