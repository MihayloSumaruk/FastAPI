from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.blog import router as blog_router
from app.api.auth import router as auth_router 

app = FastAPI(title="My Lab 5 API: Async & Auth")

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(blog_router, prefix="/blog", tags=["Blog Content"])

@app.get("/")
async def root():  
    return {"status": "Async and Auth are working!"}