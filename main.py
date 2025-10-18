from __future__ import annotations

import uvicorn
from contextlib import asynccontextmanager

from app.services.orders_service import OrdersService
from app.adapters.rest_api import app, mount_routes
from app.adapters.grpc_server import start_grpc_server

svc = OrdersService()


@asynccontextmanager
async def lifespan(app_):
    app_.state.grpc_server = await start_grpc_server(svc, port=50051)
    yield
    await app_.state.grpc_server.stop(grace=None)


app.router.lifespan_context = lifespan
mount_routes(app, svc)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
