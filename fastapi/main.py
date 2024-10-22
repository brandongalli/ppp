from fastapi import FastAPI
from contextlib import asynccontextmanager

from db_config import engine, init_db
from auth.views import router as auth_router
from player.views import router as player_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_db()
    print("Database Initialized")
    
    # Yield control to FastAPI
    yield
    
    # Shutdown logic
    print("Shutting down application...")
    engine.dispose()  # Close all database connections

app = FastAPI(lifespan=lifespan)

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "OK!"}

app.include_router(auth_router)
app.include_router(player_router)
