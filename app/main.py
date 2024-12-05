from fastapi import FastAPI # type: ignore
from app.api import endpoints
from app.api import newspaper_endpoints
from app.api import activities_creation_endpoint

app = FastAPI()

# Include API routes
app.include_router(endpoints.router)
app.include_router(newspaper_endpoints.router)
app.include_router(activities_creation_endpoint.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Cognitive Health Improving Activity Service", "v": 1.0}

# Main entry point for the application
if __name__ == "__main__":
    import uvicorn
    #uvicorn.run(app, host="127.0.0.1", port=8000)