from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import engine, Base
from app.api.routes import auth
from .routers import users, calculations

# Create tables on startup (for dev / tests)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Calculator Stack")

# CORS config – you can tighten this later if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"] etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve built frontend (if you build React into 'frontend' or similar)
# This is here because your previous code tried to mount StaticFiles.
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Routers
app.include_router(auth.router)          # from app.api.routes.auth
app.include_router(users.router)        # from app.routers.users
app.include_router(calculations.router) # from app.routers.calculations