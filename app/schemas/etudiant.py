
from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr


class EtudiantCreate(BaseModel):
    matricule: str
    nom: str
    prenom: str
    date_naissance: date | None = None
    email: EmailStr | None = None
    telephone: str | None = None
    adresse: str | None = None
    actif: bool = True


class EtudiantResponse(EtudiantCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
