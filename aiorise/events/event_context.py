from aiorise.api.client import HighriseWebApiClient

class EventContext:
    client: HighriseWebApiClient

    def __init__(self, client: HighriseWebApiClient):
        self.client = client
