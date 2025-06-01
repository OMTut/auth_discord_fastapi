import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes.auth import router as auth_router

# Load environment variables
load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "Auth API"),
    version=os.getenv("APP_VERSION", "1.0.0")
)

# Add CORS middleware for your frontend
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Auth API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include auth routes
app.include_router(auth_router, prefix="/auth", tags=["authentication"])

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    uvicorn.run("main:app", host=host, port=port, reload=debug)

