from starlette.middleware.cors import CORSMiddleware

from app.controllers import KHSBackend
from apis import v1

# 127.0.0.1:8074/v1/ws/dashboard/weather/openweathermap

core = KHSBackend(
    host="0.0.0.0",
    port=3090,
    title="KyungheeLIFE BACKEND 3.0",
    description="KyungheeLIFE",
    debug=False
)


core.app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    core.app.include_router(v1)
    core.start()
