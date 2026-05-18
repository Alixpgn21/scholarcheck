from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers.checker import router as checker_router
from routers.related_work import router as related_work_router

app = FastAPI(
    title="ScholarCheck API",
    description="SaaS de vérification bibliographique et de génération de Related Work",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(checker_router)
app.include_router(related_work_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "ScholarCheck"}


app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
