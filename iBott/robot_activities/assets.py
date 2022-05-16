import requests


class Asset(object):
    """
    Class to represent get assets from the robot manager console.
    Arguments:
        connection (object): Connection object to the robot manager console.
        id (string): Asset ID.
        name (string): Name of the asset.
    Attributes:
        connection (object): Connection object to the robot manager console.
        id (string): Asset ID.
        name (string): Name of the asset.
        type (string): Type of the asset.
        data (string): Data of the asset.
        username (string): Username of the asset.
        password (string): Password of the asset.
    Methods:
        get_assets(): Get assets all assets from the robot manager console.
        get_asset_by_id(): Get asset by ID from the robot manager console.
        get_asset_by_name(): Get asset by name from the robot manager console.

    """

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
            raise Exception(exception_message)

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
            raise Exception(exception_message)

        asset = response.json()
        self.id = asset['credential_id']
        self.name = asset['credential_name']
        self.type = asset['credential_type']
        if asset['credential_type'] == "Credential":
            self.username = asset['data_1']
            self.password = asset['data_2']
        else:
            self.data = asset['data_1']


