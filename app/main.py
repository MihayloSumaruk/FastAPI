from fastapi import FastAPI
from app.api.users import router as users_router

app = FastAPI(title="Lab 3 - FastAPI CRUD")

app.include_router(users_router)

@app.get("/")
def root():
    return {"message": "API is working. Go to /docs for Swagger UI"}