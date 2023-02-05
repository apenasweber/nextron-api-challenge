import uvicorn
from api import endpoints
from fastapi import FastAPI

from core.database import get_db

app = FastAPI()


@app.on_event("startup")
async def startup():
    """Startup event handler to create database connection"""
    # Initialize database connection
    get_db()


@app.on_event("shutdown")
async def shutdown():
    """Shutdown event handler to close database connection"""
    # Close database connection
    get_db().conn.close()

app.include_router(endpoints.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
