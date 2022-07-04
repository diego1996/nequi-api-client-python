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
class ValidateClientResponse:
    availableLimit: str
    customerName: str


class ValidateClientAPI:
    _rest_endpoint: str

    def __init__(self):
        self._rest_endpoint = '/agents/v2/-services-clientservice-validateclient'

    def _call(self, phone: str, value: float) -> ValidateClientResponse:
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
                        'ServiceName': 'RechargeService',
                        'ServiceOperation': 'validateClient',
                        'ServiceRegion': 'C001',
                        'ServiceVersion': '1.4.0'
                    }
                },
                'RequestBody': {
                    'any': {
                        'validateClientRQ': {
                            'phoneNumber': phone,
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
                    rs = ValidateClientResponse(
                        **data.ResponseMessage.ResponseBody.any['validateClientRS']
                    )
                    print(
                        "Cliente validado correctamente: "
                        f"\nLimite disponible: {rs.availableLimit} "
                        f"\nNombre: {rs.customerName}"
                    )
                    return rs
                else:
                    raise Exception(f'Error, StatusCode: {status_code} - StatusDesc: {status_desc}')
            else:
                raise Exception('Unable to connect to Nequi, please check the information sent.')
        except Exception as e:
            raise e

    def validate_client(self, phone: str, value: float) -> ValidateClientResponse | None:
        try:
            return self._call(phone, value)
        except Exception as e:
            print(f'Depositos y retiros -> Error validando cliente -> {e}')
            return None
