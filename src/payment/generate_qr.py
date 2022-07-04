import json
import secrets
import requests
from datetime import datetime
from src.auth import auth_token
from src.app_config import config
from src.utils import constants
from src.utils.responses import NequiResponse


class GenerateQRAPI:
    _rest_endpoint: str

    def __init__(self):
        self._rest_endpoint = '/payments/v2/-services-paymentservice-generatecodeqr'

    def _call(self, code: str, value: float) -> str:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': auth_token.get_token(),
            'x-api-key': config.api_key
        }
        data = {
            'RequestMessage': {
                'RequestHeader': {
                    'Channel': constants.NEQUI_CHANNEL_QR_PAYMENTS,
                    'RequestDate': datetime.now().strftime('%Y-%m-%dT%H:%M:%S0Z'),
                    'MessageID': secrets.token_hex(5),
                    'ClientID': constants.CLIENT_ID,
                    'Destination': {
                        'ServiceName': 'PaymentsService',
                        'ServiceOperation': 'generateCodeQR',
                        'ServiceRegion': constants.NEQUI_SERVICE_REGION,
                        'ServiceVersion': '1.2.0'
                    }
                },
                'RequestBody': {
                    'any': {
                        'generateCodeQRRQ': {
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
                if status_code == constants.NEQUI_STATUS_CODE_SUCCESS:
                    code_rs = data.ResponseMessage.ResponseBody.any.get('generateCodeQRRS', {})
                    code_qr = code_rs.get('codeQR', None)
                    print(f"Código QR generado correctamente -> QR Code String: {code_qr}")
                    return code_qr
                else:
                    raise Exception(f'Error, StatusCode: {status_code} - StatusDesc: {status_desc}')
            else:
                raise Exception('Unable to connect to Nequi, please check the information sent.')
        except Exception as e:
            raise e

    def generate_code(self, code: str, value: float, full: bool = True) -> str:
        try:
            code = self._call(code, value)
            return f'bancadigital-{code}' if full else code
        except Exception as e:
            print(f'Pagos con QR code -> Error generando el código -> {e}')
            return ''
