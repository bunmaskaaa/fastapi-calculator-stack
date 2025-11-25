from fastapi import FastAPI

from app.db.database import Base, engine, get_db

# Create tables on startup (for now; later you might use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Calculator Stack - Module 11")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Calculator backend running"}