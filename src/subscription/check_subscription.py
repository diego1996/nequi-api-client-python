import json
import secrets
import requests
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from src.auth import auth_token
from src.app_config import config
from src.utils import constants
from src.utils.responses import NequiResponse


@dataclass
class CheckSubscriptionResponse:
    dateCreated: str
    name: str
    status: str
    merchantId: str
    namePocket: Optional[str]
    region: Optional[str]


class CheckSubscriptionAPI:
    _rest_endpoint: str

    def __init__(self):

        self._rest_endpoint = '/subscriptions/v2/-services-subscriptionpaymentservice-getsubscription'

    def _call(self, phone_number: str, code: str, token: str) -> CheckSubscriptionResponse:
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
                        'ServiceOperation': 'getSubscription',
                        'ServiceRegion': constants.NEQUI_SERVICE_REGION,
                        'ServiceVersion': '1.0.0'
                    }
                },
                'RequestBody': {
                    'any': {
                        'getSubscriptionRQ': {
                            'phoneNumber': phone_number,
                            'code': code,
                            'token': token
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
                    rs = CheckSubscriptionResponse(
                        **data.ResponseMessage.ResponseBody.any['getSubscriptionRS']['subscription']
                    )
                    print(
                        f"Subscripción consultada correctamente -> "
                        f"\nNombre: {rs.name}"
                        f"\nFecha: {rs.dateCreated}"
                        f"\nEstado: {rs.status}"
                    )
                    return rs
                else:
                    raise Exception(f'Error, StatusCode: {status_code} - StatusDesc: {status_desc}')
            else:
                raise Exception('Unable to connect to Nequi, please check the information sent.')
        except Exception as e:
            raise e

    def check_subscription(self, phone_number: str, code: str, token: str) -> CheckSubscriptionResponse | None:
        try:
            return self._call(phone_number, code, token)
        except Exception as e:
            print(f'Pagos con suscripción -> Error consultado la subscripción -> {e}')
            return None
