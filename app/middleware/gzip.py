from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware


def add_gzip_middleware(app: FastAPI, minimum_size: int = 500):
    app.add_middleware(GZipMiddleware, minimum_size=minimum_size)
