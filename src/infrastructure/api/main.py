from fastapi import FastAPI
from infrastructure.api.routers import users, tracking

app = FastAPI()

app.include_router(users.router)
app.include_router(tracking.router)

@app.get("/")
def root():
    return {"message": "Server is running!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
