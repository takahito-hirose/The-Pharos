from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="The Pharos - ARK Independent Quality Audit System",
    version="1.0.0"
)

# 🌟 Phase 16 Step 4 (HUD連携) のためのCORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境ではHUDのURLに絞るわよ💋
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "status": "online",
        "system": settings.APP_NAME,
        "message": "The Pharos is watching over the code."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) # 文字列指定でホットリロードを有効化💋