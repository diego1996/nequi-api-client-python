import json
import secrets
import requests
from typing import List
from dataclasses import dataclass
from datetime import datetime
from src.auth import auth_token
from src.app_config import config
from src.utils import constants
from src.utils.responses import NequiResponse


@dataclass
class _Transaction:
    buyerLastName: str
    transactionDate: str
    commerceName: str
    buyerName: str
    productChannel: str
    transactionReference: str
    messageId: str
    transactionValue: str


@dataclass
class ReportResponse:
    commerce: str
    nit: str
    total: str
    count: str
    accountNumber: List[str]
    transactions: List[_Transaction]


class ReportAPI:
    _rest_endpoint: str

    def __init__(self):
        self._status = ''
        self._rest_endpoint = '/partners/v2/-services-reportsservice-getreports'

    def _call(self, code: str, start_date: str, end_date: str, format_: str) -> ReportResponse | None:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': auth_token.get_token(),
            'x-api-key': config.api_key
        }
        data = {
            'RequestMessage': {
                'RequestHeader': {
                    'Channel': constants.NEQUI_CHANNEL_REPORTS,
                    'RequestDate': datetime.now().strftime('%Y-%m-%dT%H:%M:%S0Z'),
                    'MessageID': secrets.token_hex(5),
                    'ClientID': constants.CLIENT_ID,
                    'Destination': {
                        'ServiceName': 'ReportsService',
                        'ServiceOperation': 'getReports',
                        'ServiceRegion': constants.NEQUI_SERVICE_REGION,
                        'ServiceVersion': '1.0.0'
                    }
                },
                'RequestBody': {
                    'any': {
                        'getReportsRQ': {
                            'code': code,
                            'startDate': start_date,
                            'endDate': end_date,
                            'format': format_
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
                    rs_report = data.ResponseMessage.ResponseBody.any.get('getReportsRS', {})
                    if 'reportURL' in rs_report.keys():
                        report_url = rs_report['reportURL'] if rs_report['reportURL'] else None
                        print(
                            "Consulta de reporte realizada correctamente: "
                            f"\nURL Reporte: {report_url} "
                        )
                        return report_url
                    rs = ReportResponse(
                        **rs_report
                    )
                    print(
                        "Consulta de reporte realizada correctamente: "
                        f"\nComercio: {rs.commerce} "
                        f"\nNIT: {rs.nit} "
                        f"\nTotal: {rs.total} "
                        f"\nCantidad: {rs.count} "
                        f"\nTransacciones: {len(rs.transactions)} "
                    )
                    return rs
                else:
                    raise Exception(f'Error, StatusCode: {status_code} - StatusDesc: {status_desc}')
            else:
                raise Exception('Unable to connect to Nequi, please check the information sent.')
        except Exception as e:
            raise e

    def get_report(self, code: str, start_date: str, end_date: str, format_: str = 'json') -> ReportResponse | None:
        try:
            return self._call(code, start_date, end_date, format_)
        except Exception as e:
            print(f'Servicios de reportes -> Error obteniendo el reporte -> {e}')
            return None
