from fastapi import APIRouter, FastAPI

app = FastAPI(title="Teste")

docs_router = APIRouter()

app.include_router(docs_router)


@app.get("/")
def root():
    return {"message": "ok"}
