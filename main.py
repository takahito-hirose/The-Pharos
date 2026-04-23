# ARK_MEMORY_SYSTEM_ACTIVE
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router

app = FastAPI(
    title="The Pharos",
    description="The Pharos - ARK Independent Quality Audit System",
    version="1.0.0"
)

# Add CORS middleware as requested
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router. A prefix is good practice for versioning.
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """
    Root endpoint to check if the API is online.
    """
    return {
        "status": "online",
        "system": "The Pharos",
        "message": "The Pharos is watching over the code."
    }

if __name__ == "__main__":
    import uvicorn
    # Running with uvicorn for development. reload=True enables hot-reloading.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)