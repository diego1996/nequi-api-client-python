from app_config import config
from src.reports import ReportAPI

if not config.client_id:
    raise Exception(
        'The NEQUI_CLIENT_ID setting must have some value'
    )

if not config.client_secret:
    raise Exception(
        'The NEQUI_CLIENT_SECRET setting must have some value'
    )

if not config.api_key:
    raise Exception(
        'The NEQUI_API_KEY setting must have some value'
    )

if not config.auth_uri:
    raise Exception(
        'The NEQUI_AUTH_URI setting must have some value'
    )

if not config.auth_grant_type:
    raise Exception(
        'The NEQUI_AUTH_GRANT_TYPE setting must have some value'
    )

if not config.api_base_path:
    raise Exception(
        'The NEQUI_API_BASE_PATH setting must have some value'
    )

print("¡Felicitaciones!, la configuración básica es la adecuada")

x = ReportAPI()
x.get_report('NIT_1', '2018-09-01', '2018-09-09', 'pdf')
