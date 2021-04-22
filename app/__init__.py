from fastapi import FastAPI

def server(title: str, description: str, debug: bool = False):
    core = FastAPI(
        debug=debug,
        title=title,
        description=description
    )
    return core

