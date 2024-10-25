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
    """
    Context manager for application lifespan.
    
    Initializes the database at startup and disposes of the database engine on shutdown.
    """
    # Initialize the database at application startup
    init_db()
    print("Database Initialized")

    yield
    
    # Perform shutdown operations
    print("Shutting down application...")
    engine.dispose()  # Close all database connections

# Define the FastAPI application with lifespan context and custom documentation URLs
app = FastAPI(
    lifespan=lifespan,
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    openapi_url="/v1/openapi.json",
)

# Set allowed CORS origins
origins = [
    "http://localhost:3000",
]

# Add CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthcheck")
async def healthcheck():
    """
    Health check endpoint to verify the service status.
    
    Returns:
    - {"status": "OK!"}: JSON response confirming service is active.
    """
    return {"status": "OK!"}

@app.post('/populate-db')
async def populate_data(_: bool = Depends(authorization)):
    """
    Populate the database with mock data for testing or development.
    
    Authorization is required to access this endpoint.
    
    Returns:
    - Result of the populate_database function.
    """
    return populate_database()

# Include routers for different modules
app.include_router(auth_router)
app.include_router(player_router)
app.include_router(game_router)
