from fastapi import FastAPI
from app.database import db
from app.routers.users import router as user_router

app = FastAPI()

# Startup and Shutdown events
@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# Include routers
app.include_router(user_router, prefix="/users", tags=["Users"])
