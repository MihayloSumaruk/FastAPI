from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.blog import router as blog_router # Новий роутер

app = FastAPI(title="My Lab 4 Blog API")

app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(blog_router, prefix="/blog", tags=["Blog Content"])

app.get("/")
async def root():  
    return {"status": "Async is working!"}
