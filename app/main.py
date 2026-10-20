
from fastapi import FastAPI

from app.routers.etudiants import router as etudiants_router

app = FastAPI(
    title="API de gestion de scolarité",
    description="API REST pour gérer les étudiants, les formations et les inscriptions.",
    version="1.0.0"
)

app.include_router(etudiants_router)


@app.get("/")
def accueil():
    return {
        "message": "Bienvenue dans l'API de gestion de scolarité"
    }


@app.get("/health")
def verifier_etat():
    return {"status": "ok"}
