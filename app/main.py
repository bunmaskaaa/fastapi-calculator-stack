from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import Base
from app.database import engine
from app.routers import users, calculations

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Calculator Stack (outer app)")


# ---------- CORS ----------

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- ROOT ----------

@app.get("/")
def read_root():
    return {"message": "API is running from OUTER app.main"}


# ---------- ROUTERS ----------

# users endpoints (used by pytest)
app.include_router(users.router, prefix="/users", tags=["users"])

# calculations BREAD endpoints at /calculations/
app.include_router(calculations.router, prefix="/calculations", tags=["calculations"])