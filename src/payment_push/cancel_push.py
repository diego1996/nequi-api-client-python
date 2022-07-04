import json
import secrets
import requests
from datetime import datetime
from src.auth import auth_token
from src.app_config import config
from src.utils import constants
from src.utils.responses import NequiResponse


class CancelPushAPI:
    _rest_endpoint: str

    def __init__(self):
        self._rest_endpoint = '/payments/v2/-services-paymentservice-cancelunregisteredpayment'

    def _call(self, phone_number: str, code: str, transaction_id: str) -> bool:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': auth_token.get_token(),
            'x-api-key': config.api_key
        }
        data = {
            'RequestMessage': {
                'RequestHeader': {
                    'Channel': constants.NEQUI_CHANNEL_PUSH_PAYMENTS,
                    'RequestDate': datetime.now().strftime('%Y-%m-%dT%H:%M:%S0Z'),
                    'MessageID': secrets.token_hex(5),
                    'ClientID': constants.CLIENT_ID,
                    'Destination': {
                        'ServiceName': 'PaymentsService',
                        'ServiceOperation': 'unregisteredPayment',
                        'ServiceRegion': constants.NEQUI_SERVICE_REGION,
                        'ServiceVersion': '1.0.0'
                    }
                },
                'RequestBody': {
                    'any': {
                        'cancelUnregisteredPaymentRQ': {
                            'phoneNumber': phone_number,
                            'code': code,
                            'transactionId': transaction_id
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
                    rs = data.ResponseMessage.ResponseBody.any.get('cancelRequestMoneyRS', {})
                    print(f"Notificatión Push cancelada correctamente -> Data: {rs}")
                    return True
                else:
                    raise Exception(f'Error, StatusCode: {status_code} - StatusDesc: {status_desc}')
            else:
                raise Exception('Unable to connect to Nequi, please check the information sent.')
        except Exception as e:
            raise e

    def cancel_push(self, phone_number: str, code: str, transaction_id: str) -> bool:
        try:
            return self._call(phone_number, code, transaction_id)
        except Exception as e:
            print(f'Pagos con Notificación -> Error cancelando la notificación push -> {e}')
            return False
