from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from db_config import engine, init_db
from mock_data import populate_database
from auth.provider import authorization
from auth.views import router as auth_router
from player.views import router as player_router
from game.views import router as game_router

@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()
    print("Database Initialized")

    yield
    
    # Shutdown logic
    print("Shutting down application...")
    engine.dispose()  # Close all database connections

app = FastAPI(
    lifespan=lifespan,
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    openapi_url="/v1/openapi.json",
)

# Set API info
app = FastAPI(
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    openapi_url="/v1/openapi.json",
)

# Set CORS
origins = [
    "http://localhost:3000",
]

# Set middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "OK!"}

@app.post('/populate-db')
async def populate_data(_: bool = Depends(authorization)):
    return populate_database()

app.include_router(auth_router)
app.include_router(player_router)
app.include_router(game_router)