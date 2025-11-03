from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import os

app = FastAPI(title="FastAPI Calculator")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/fastapi_db")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

class CalcIn(BaseModel):
    operation: str
    a: float
    b: float

@app.get("/health")
def health():
    # Quick DB round-trip
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}

@app.post("/calc")
def calc(body: CalcIn):
    if body.operation == "add":
        result = body.a + body.b
    elif body.operation == "subtract":
        result = body.a - body.b
    elif body.operation == "multiply":
        result = body.a * body.b
    elif body.operation == "divide":
        result = body.a / body.b
    else:
        return {"error": "unknown operation"}
    return {"operation": body.operation, "a": body.a, "b": body.b, "result": result}