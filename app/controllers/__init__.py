import uvicorn
from fastapi import FastAPI


class KHSBackend:
    def __init__(self, host: str, port: int, title: str, description: str, debug: bool = False) -> None:
        self.host = host
        self.port = port
        self.app = self.server(title=title, description=description, debug=debug)

    @staticmethod
    def server(title: str, description: str, debug: bool) -> FastAPI:
        core = FastAPI(
            debug=debug,
            title=title,
            description=description
        )
        return core

    def start(self):
        uvicorn.run(self.app, host=self.host, port=self.port)
