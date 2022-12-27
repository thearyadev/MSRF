import pocketbase


class DatabaseConfig(pocketbase.PocketBase):
    def __init__(self, url: str):
        super().__init__(url)
