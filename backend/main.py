from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback
import models
import database
from routes import auth, citizen, schemes, chat

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Citizen Digital DNA API",
    description="Backend for Citizen Digital DNA Hackathon Project",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://localhost:8082",
        "http://127.0.0.1:8082",
        "http://localhost:19006",
    ],
    allow_origin_regex="http://192\.168\..*", # Allow local network IPs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("GLOBAL EXCEPTION CAUGHT:")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "message": str(exc)},
    )

app.include_router(auth.router)
app.include_router(citizen.router)
app.include_router(schemes.router)
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Citizen Digital DNA API"}
