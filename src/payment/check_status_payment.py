import json
import secrets
from typing import Optional

import requests
from dataclasses import dataclass
from datetime import datetime
from src.auth import auth_token
from src.app_config import config
from src.utils import constants
from src.utils.responses import NequiResponse


@dataclass
class CheckStatusQRPaymentResponse:
    status: str
    name: str
    value: str
    date: str
    trnId: str
    ipAddress: str
    originMoney: Optional[dict] = None


class CheckStatusQRPaymentAPI:
    _rest_endpoint: str

    def __init__(self):
        self._rest_endpoint = '/payments/v2/-services-paymentservice-getstatuspayment'

    def _call(self, code_qr: str) -> CheckStatusQRPaymentResponse:
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
                        'ServiceOperation': 'getStatusPayment',
                        'ServiceRegion': 'C001',
                        'ServiceVersion': '1.0.0'
                    }
                },
                'RequestBody': {
                    'any': {
                        'getStatusPaymentRQ': {
                            'codeQR': code_qr
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
                    rs = CheckStatusQRPaymentResponse(
                        **data.ResponseMessage.ResponseBody.any['getStatusPaymentRS']
                    )
                    print(
                        "Consulta de estado de pago realizada correctamente: "
                        f"\nNombre: {rs.name} "
                        f"\nEstado: {rs.status} "
                        f"\nValor: {rs.value} "
                        f"\nFecha: {rs.date} "
                        f"\nDirección IP: {rs.ipAddress} "
                        f"\nID de transacción: {rs.trnId} "
                    )
                    return rs
                else:
                    raise Exception(f'Error, StatusCode: {status_code} - StatusDesc: {status_desc}')
            else:
                raise Exception('Unable to connect to Nequi, please check the information sent.')
        except Exception as e:
            raise e

    def get_status_payment(self, code_qr: str) -> CheckStatusQRPaymentResponse | None:
        try:
            return self._call(code_qr)
        except Exception as e:
            print(f'Pagos con QR code -> Error verificando estado del pago con QR -> {e}')
            return None
