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
class CheckStatusPushPaymentResponse:
    status: str
    name: str
    value: str
    date: str
    trnId: str
    ipAddress: str
    originMoney: Optional[dict] = None


class CheckStatusPushPaymentAPI:
    _rest_endpoint: str
    _status: str

    def __init__(self):
        self._status = ''
        self._rest_endpoint = '/payments/v2/-services-paymentservice-getstatuspayment'

    def _call(self, transaction_id: str) -> CheckStatusPushPaymentResponse:
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
                        'ServiceOperation': 'getStatusPayment',
                        'ServiceRegion': constants.NEQUI_SERVICE_REGION,
                        'ServiceVersion': '1.0.0'
                    }
                },
                'RequestBody': {
                    'any': {
                        'getStatusPaymentRQ': {
                            'codeQR': transaction_id
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
                    rs = CheckStatusPushPaymentResponse(
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
                    self._status = rs.status
                    return rs
                else:
                    raise Exception(f'Error, StatusCode: {status_code} - StatusDesc: {status_desc}')
            else:
                raise Exception('Unable to connect to Nequi, please check the information sent.')
        except Exception as e:
            raise e

    def validate_status(self):
        if self._status == constants.NEQUI_PAYMENT_STATUS_CODE_PENDING:
            return constants.NEQUI_PAYMENT_STATUS_DESC_PENDING
        if self._status == constants.NEQUI_PAYMENT_STATUS_CODE_SUCCESS:
            return constants.NEQUI_PAYMENT_STATUS_DESC_SUCCESS
        return constants.NEQUI_PAYMENT_STATUS_DESC_UNKNOWN

    def get_status_payment(self, transaction_id: str) -> CheckStatusPushPaymentResponse | None:
        try:
            return self._call(transaction_id)
        except Exception as e:
            print(f'Pagos con Notificación -> Error verificando estado del pago con notificación push -> {e}')
            return None
