
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Etudiant
from app.schemas.etudiant import EtudiantCreate, EtudiantResponse

router = APIRouter(
    prefix="/etudiants",
    tags=["Étudiants"]
)


@router.get("/", response_model=list[EtudiantResponse])
def lister_etudiants(db: Session = Depends(get_db)):
    return db.query(Etudiant).all()


@router.post(
    "/",
    response_model=EtudiantResponse,
    status_code=status.HTTP_201_CREATED
)
def creer_etudiant(
    donnees: EtudiantCreate,
    db: Session = Depends(get_db)
):
    matricule_existant = (
        db.query(Etudiant)
        .filter(Etudiant.matricule == donnees.matricule)
        .first()
    )

    if matricule_existant:
        raise HTTPException(
            status_code=409,
            detail="Ce matricule existe déjà."
        )

    email_existant = None

    if donnees.email:
        email_existant = (
            db.query(Etudiant)
            .filter(Etudiant.email == str(donnees.email))
            .first()
        )

    if email_existant:
        raise HTTPException(
            status_code=409,
            detail="Cet e-mail est déjà utilisé."
        )

    nouvel_etudiant = Etudiant(
        **donnees.model_dump(mode="json")
    )

    db.add(nouvel_etudiant)
    db.commit()
    db.refresh(nouvel_etudiant)

    return nouvel_etudiant


@router.get("/{etudiant_id}", response_model=EtudiantResponse)
def obtenir_etudiant(
    etudiant_id: int,
    db: Session = Depends(get_db)
):
    etudiant = (
        db.query(Etudiant)
        .filter(Etudiant.id == etudiant_id)
        .first()
    )

    if etudiant is None:
        raise HTTPException(
            status_code=404,
            detail="Étudiant introuvable."
        )

    return etudiant


@router.put("/{etudiant_id}", response_model=EtudiantResponse)
def modifier_etudiant(
    etudiant_id: int,
    donnees: EtudiantCreate,
    db: Session = Depends(get_db)
):
    # Rechercher l'étudiant
    etudiant = (
        db.query(Etudiant)
        .filter(Etudiant.id == etudiant_id)
        .first()
    )

    # Vérifier si l'étudiant existe
    if etudiant is None:
        raise HTTPException(
            status_code=404,
            detail="Étudiant introuvable."
        )

    # Vérifier si le matricule est déjà utilisé
    matricule_existant = (
        db.query(Etudiant)
        .filter(
            Etudiant.matricule == donnees.matricule,
            Etudiant.id != etudiant_id
        )
        .first()
    )

    if matricule_existant:
        raise HTTPException(
            status_code=409,
            detail="Ce matricule est déjà utilisé par un autre étudiant."
        )

    # Vérifier si l'e-mail est déjà utilisé
    if donnees.email:
        email_existant = (
            db.query(Etudiant)
            .filter(
                Etudiant.email == str(donnees.email),
                Etudiant.id != etudiant_id
            )
            .first()
        )

        if email_existant:
            raise HTTPException(
                status_code=409,
                detail="Cet e-mail est déjà utilisé par un autre étudiant."
            )

    # Modifier les informations
    for champ, valeur in donnees.model_dump(mode="json").items():
        setattr(etudiant, champ, valeur)

    # Enregistrer les modifications
    db.commit()
    db.refresh(etudiant)

    return etudiant


