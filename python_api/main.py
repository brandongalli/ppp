from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from user.routers import router as user_router
from auth.routers import router as auth_router

# Set API info
app = FastAPI(
    title="Example API",
    description="This is an example API of FastAPI",
    contact={
        "name": "Masaki Yoshiiwa",
        "email": "masaki.yoshiiwa@gmail.com",
    },
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


"""
Auth APIs
Provides sign-up, sign-in, and refresh-token APIs.
"""

app.include_router(auth_router)


"""
User APIs
Provides user CRUD APIs.
"""

app.include_router(user_router)
