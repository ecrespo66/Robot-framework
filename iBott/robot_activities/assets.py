import requests

from iBott.robot_activities.server import OrchestratorAPI


class Asset(OrchestratorAPI):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super().__init__(**self.kwargs)
        self.assetsid = self.kwargs.get('assets_id', None)
        self.assets_name = self.kwargs.get('assets_name', None)
        self.assets_type = self.kwargs.get('assets_type', None)
        self.data = self.kwargs.get('data', None)
        self.username = self.kwargs.get('username', None)
        self.password = self.kwargs.get('password', None)


    def get_assets(self):
        endpoint = f"{self.http_protocol}{self.url}/api/assets/"
        response = requests.get(endpoint, headers=self.headers)
        return response.json()
