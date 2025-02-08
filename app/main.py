from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.v1 import router as v1_api

app = FastAPI(
    title="Todo Application",
    # ORJSONResponse как дефолтный обработчик json'а.
    # 10x быстрее в задаче .dumps()
    # 2x быстрее в задаче .loads()
    default_response_class=ORJSONResponse,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://todo.efinskiy.ru"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(v1_api)
