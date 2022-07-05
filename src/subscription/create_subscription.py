import json
import secrets
import requests
from datetime import datetime
from src.auth import auth_token
from src.app_config import config
from src.utils import constants
from src.utils.responses import NequiResponse


class CreateSubscriptionAPI:
    _rest_endpoint: str

    def __init__(self):
        self._rest_endpoint = '/subscriptions/v2/-services-subscriptionpaymentservice-newsubscription'

    def _call(self, phone_number: str, code: str, name: str) -> str:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': auth_token.get_token(),
            'x-api-key': config.api_key
        }
        data = {
            'RequestMessage': {
                'RequestHeader': {
                    'Channel': constants.NEQUI_CHANNEL_SUBSCRIPTIONS_PAYMENTS,
                    'RequestDate': datetime.now().strftime('%Y-%m-%dT%H:%M:%S0Z'),
                    'MessageID': secrets.token_hex(5),
                    'ClientID': constants.CLIENT_ID,
                    'Destination': {
                        'ServiceName': 'SubscriptionPaymentService',
                        'ServiceOperation': 'newSubscription',
                        'ServiceRegion': constants.NEQUI_SERVICE_REGION,
                        'ServiceVersion': '1.0.0'
                    }
                },
                'RequestBody': {
                    'any': {
                        'newSubscriptionRQ': {
                            'phoneNumber': phone_number,
                            'code': code,
                            'name': name
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
                    subscription_rs = data.ResponseMessage.ResponseBody.any.get('newSubscriptionRS', {})
                    token = subscription_rs.get('token', None)
                    print(f"Subscripción creada correctamente -> Token: {token}")
                    return token
                else:
                    raise Exception(f'Error, StatusCode: {status_code} - StatusDesc: {status_desc}')
            else:
                raise Exception('Unable to connect to Nequi, please check the information sent.')
        except Exception as e:
            raise e

    def create_subscription(self, phone_number: str, code: str, name: str) -> str:
        try:
            return self._call(phone_number, code, name)
        except Exception as e:
            print(f'Pagos con suscripción -> Error creando la subscripción -> {e}')
            return ''
