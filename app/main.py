from fastapi import FastAPI # type: ignore
from app.api import endpoints

app = FastAPI()

# Include API routes
app.include_router(endpoints.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Cognitive Health Improving Activity Service"}
