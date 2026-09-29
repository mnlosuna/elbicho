from contextlib import asynccontextmanager
import socket

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import create_db_and_tables
from elbicho.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
	create_db_and_tables()
	local_ip = socket.gethostbyname(socket.gethostname())
	print(f"API disponible en http://{local_ip}:8000")
	print(f"Documentacion: http://{local_ip}:8000/docs")
	yield


app = FastAPI(
	title="FastAPI Osuna",
	description="API de usuarios con FastAPI y SQLModel",
	version="1.0.0",
	lifespan=lifespan,
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=False,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(users_router)


@app.get("/")
def root():
	return {"message": "¡Bienvenido a FastAPI Osuna!"}


@app.get("/health")
def health_check():
	return {"status": "healthy"}


if __name__ == "__main__":
	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)