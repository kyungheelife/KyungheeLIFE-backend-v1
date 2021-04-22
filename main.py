import uvicorn
from app import server
from apis import v1

from starlette.middleware.cors import CORSMiddleware

app = server(
    title="KyungheeLIFE BACKEND 3.0",
    description="KyungheeLIFE",
    debug=False
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    app.include_router(v1)
    uvicorn.run(app, host="0.0.0.0", port=8074)
