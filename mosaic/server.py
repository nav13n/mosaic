import uuid
import io
import os
import logging
import json

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import (
    BaseModel,
    confloat
)
from enum import Enum
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from typing import Union, List, Any

from .config import API_V1_STR, OPENAPI_PREFIX, ALLOWED_HOSTS, SERVICE_NAME, SERVICE_VERSION
from .api import mosaic

app = FastAPI(
    title="Mosaic Service",
    description="API for Mosaic: A template based dynamic image generation service",
    version=SERVICE_VERSION,
    root_path=OPENAPI_PREFIX,
    openapi_prefix=OPENAPI_PREFIX,
)

log = logging.getLogger("app")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    mosaic.router,
    prefix=API_V1_STR,
    tags=["Mosaic Service"],
)

@app.get("/")
def read_root():
    return {"version": "0.1","name":"Mosaic: A template based image generation service"}


@app.get("/health")
async def system_health():
    return {"status": "ok"}


@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(request, exc):
    log.error(f"ERROR:{exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"{exc.detail}"},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    log.error(f"ERROR:{exc}")
    return JSONResponse(
        status_code=400,
        content={"message": f"{str(exc)}"},
    )






