from fastapi import FastAPI
from api.routes import router as api_router
from core.config import settings

app = FastAPI(title=settings.APP_NAME)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME} API"}

# The following block is for development purposes.
# In a production environment, you would use a WSGI server like Uvicorn or Gunicorn
# to run the application, e.g., `uvicorn main:app --reload`.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)