from fastapi import FastAPI
app = FastAPI(title="Lab 1 API")
@app.get("/")
def read_root(): return {"message": "Lab 1 Template"}