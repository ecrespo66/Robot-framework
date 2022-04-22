import requests
from iBott import OrchestratorConnectionError


class Asset(object):

    def __init__(self, **kwargs):
        self.connection = kwargs['connection']
        self.id = kwargs.get('asset_id', None)
        self.name = kwargs.get('asset_name', None)

        self.type = None
        self.data = None
        self.username = None
        self.password = None

        if self.id:
            self.get_asset_by_id()
        elif self.name:
            self.get_asset_by_name()
        else:
            raise ValueError('You must provide either assets_id or assets_name')

    def get_assets(self):
        endpoint = f"{self.connection.http_protocol}{self.connection.url}/api/assets/"
        response = requests.get(endpoint, headers=self.connection.headers)
        return response.json()

    def get_asset_by_name(self):
        endpoint = f"{self.connection.http_protocol}{self.connection.url}/api/assets/asset_name={self.name}"
        try:
            response = requests.get(endpoint, headers=self.connection.headers)
        except Exception as exception_message:
            raise OrchestratorConnectionError(exception_message)

        asset = response.json()
        self.id = asset['asset_id']
        self.name = asset['asset_name']
        self.type = asset['asset_type']
        if self.type == "Credential":
            self.username = asset['data_1']
            self.password = asset['data_2']
        else:
            self.data = asset['data_1']

    def get_asset_by_id(self):
        endpoint = f"{self.connection.http_protocol}{self.connection.url}/api/assets/credential_id={self.id}"
        try:
            response = requests.get(endpoint, headers=self.connection.headers)
        except Exception as exception_message:
            raise OrchestratorConnectionError(exception_message)

        asset = response.json()
        self.id = asset['credential_id']
        self.name = asset['credential_name']
        self.type = asset['credential_type']
        if asset['credential_type'] == "Credential":
            self.username = asset['data_1']
            self.password = asset['data_2']
        else:
            self.data = asset['data_1']


