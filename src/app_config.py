import os


class AppConf:
    client_id: str = None
    client_secret: str = None
    api_key: str = None
    auth_uri: str = None
    auth_grant_type: str = None
    api_base_path: str = None

    def __init__(self):
        self.load_env_vars()

    def load_env_vars(self):
        self.client_id = os.getenv('NEQUI_CLIENT_ID', None)
        self.client_secret = os.getenv('NEQUI_CLIENT_SECRET', None)
        self.api_key = os.getenv('NEQUI_API_KEY', None)

        self.auth_uri = os.getenv('NEQUI_AUTH_URI', None)
        self.auth_grant_type = os.getenv('NEQUI_AUTH_GRANT_TYPE', None)
        self.api_base_path = os.getenv('NEQUI_API_BASE_PATH', None)


config = AppConf()
