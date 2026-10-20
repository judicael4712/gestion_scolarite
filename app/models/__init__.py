
from datetime import date, time

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# 1. ROLES
class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    libelle: Mapped[str] = mapped_column(String(100), nullable=False)

    utilisateurs: Mapped[list["Utilisateur"]] = relationship(
        back_populates="role"
    )


# 2. UTILISATEURS
class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom_utilisateur: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False
    )
    mot_de_passe_hash: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"), nullable=False
    )
    actif: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    role: Mapped["Role"] = relationship(back_populates="utilisateurs")


# 3. FORMATIONS
class Formation(Base):
    __tablename__ = "formations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nom: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    duree_mois: Mapped[int] = mapped_column(Integer, nullable=False)
    actif: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    niveaux: Mapped[list["Niveau"]] = relationship(
        back_populates="formation"
    )


# 4. NIVEAUX
class Niveau(Base):
    __tablename__ = "niveaux"
    __table_args__ = (
        UniqueConstraint("formation_id", "ordre", name="uq_niveau_ordre"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    formation_id: Mapped[int] = mapped_column(
        ForeignKey("formations.id"), nullable=False
    )
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    ordre: Mapped[int] = mapped_column(Integer, nullable=False)

    formation: Mapped["Formation"] = relationship(
        back_populates="niveaux"
    )
    formation_matieres: Mapped[list["FormationMatiere"]] = relationship(
        back_populates="niveau"
    )
    inscriptions: Mapped[list["Inscription"]] = relationship(
        back_populates="niveau"
    )


# 5. MATIERES
class Matiere(Base):
    __tablename__ = "matieres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    nom: Mapped[str] = mapped_column(String(150), nullable=False)
    coefficient: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    volume_horaire: Mapped[int] = mapped_column(Integer, nullable=False)

    formation_matieres: Mapped[list["FormationMatiere"]] = relationship(
        back_populates="matiere"
    )


# 6. FORMATION_MATIERES
class FormationMatiere(Base):
    __tablename__ = "formation_matieres"
    __table_args__ = (
        UniqueConstraint(
            "niveau_id", "matiere_id", "semestre",
            name="uq_niveau_matiere_semestre",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    niveau_id: Mapped[int] = mapped_column(
        ForeignKey("niveaux.id"), nullable=False
    )
    matiere_id: Mapped[int] = mapped_column(
        ForeignKey("matieres.id"), nullable=False
    )
    semestre: Mapped[int] = mapped_column(Integer, nullable=False)

    niveau: Mapped["Niveau"] = relationship(
        back_populates="formation_matieres"
    )
    matiere: Mapped["Matiere"] = relationship(
        back_populates="formation_matieres"
    )
    cours: Mapped[list["Cours"]] = relationship(
        back_populates="formation_matiere"
    )
    evaluations: Mapped[list["Evaluation"]] = relationship(
        back_populates="formation_matiere"
    )


# 7. ENSEIGNANTS
class Enseignant(Base):
    __tablename__ = "enseignants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    matricule: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    prenom: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False
    )
    telephone: Mapped[str | None] = mapped_column(
        String(30), nullable=True
    )

    cours: Mapped[list["Cours"]] = relationship(
        back_populates="enseignant"
    )


# 8. COURS
class Cours(Base):
    __tablename__ = "cours"
    __table_args__ = (
        CheckConstraint(
            "heure_fin > heure_debut",
            name="ck_cours_horaires",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    formation_matiere_id: Mapped[int] = mapped_column(
        ForeignKey("formation_matieres.id"), nullable=False
    )
    enseignant_id: Mapped[int] = mapped_column(
        ForeignKey("enseignants.id"), nullable=False
    )
    date_cours: Mapped[date] = mapped_column(Date, nullable=False)
    heure_debut: Mapped[time] = mapped_column(Time, nullable=False)
    heure_fin: Mapped[time] = mapped_column(Time, nullable=False)

    formation_matiere: Mapped["FormationMatiere"] = relationship(
        back_populates="cours"
    )
    enseignant: Mapped["Enseignant"] = relationship(
        back_populates="cours"
    )
    presences: Mapped[list["Presence"]] = relationship(
        back_populates="cours"
    )


# 9. ANNEES SCOLAIRES
class AnneeScolaire(Base):
    __tablename__ = "annees_scolaires"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    libelle: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )
    date_debut: Mapped[date] = mapped_column(Date, nullable=False)
    date_fin: Mapped[date] = mapped_column(Date, nullable=False)
    active: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )


# 10. ETUDIANTS
class Etudiant(Base):
    __tablename__ = "etudiants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    matricule: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    prenom: Mapped[str] = mapped_column(String(100), nullable=False)
    date_naissance: Mapped[date] = mapped_column(Date, nullable=False)
    email: Mapped[str | None] = mapped_column(
        String(150), unique=True, nullable=True
    )
    telephone: Mapped[str | None] = mapped_column(
        String(30), nullable=True
    )
    adresse: Mapped[str | None] = mapped_column(Text, nullable=True)
    actif: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    inscriptions: Mapped[list["Inscription"]] = relationship(
        back_populates="etudiant"
    )


# 11. INSCRIPTIONS
class Inscription(Base):
    __tablename__ = "inscriptions"
    __table_args__ = (
        UniqueConstraint(
            "etudiant_id", "niveau_id", "annee_scolaire_id",
            name="uq_inscription_etudiant_niveau_annee",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    etudiant_id: Mapped[int] = mapped_column(
        ForeignKey("etudiants.id"), nullable=False
    )
    niveau_id: Mapped[int] = mapped_column(
        ForeignKey("niveaux.id"), nullable=False
    )
    annee_scolaire_id: Mapped[int] = mapped_column(
        ForeignKey("annees_scolaires.id"), nullable=False
    )
    date_inscription: Mapped[date] = mapped_column(Date, nullable=False)
    statut: Mapped[str] = mapped_column(
        String(30), default="active", nullable=False
    )

    etudiant: Mapped["Etudiant"] = relationship(
        back_populates="inscriptions"
    )
    niveau: Mapped["Niveau"] = relationship(
        back_populates="inscriptions"
    )
    notes: Mapped[list["Note"]] = relationship(
        back_populates="inscription"
    )
    presences: Mapped[list["Presence"]] = relationship(
        back_populates="inscription"
    )


# 12. EVALUATIONS
class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    formation_matiere_id: Mapped[int] = mapped_column(
        ForeignKey("formation_matieres.id"), nullable=False
    )
    libelle: Mapped[str] = mapped_column(String(150), nullable=False)
    date_evaluation: Mapped[date] = mapped_column(Date, nullable=False)
    bareme: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False)

    formation_matiere: Mapped["FormationMatiere"] = relationship(
        back_populates="evaluations"
    )
    notes: Mapped[list["Note"]] = relationship(
        back_populates="evaluation"
    )


# 13. NOTES
class Note(Base):
    __tablename__ = "notes"
    __table_args__ = (
        UniqueConstraint(
            "evaluation_id", "inscription_id",
            name="uq_note_evaluation_inscription",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    evaluation_id: Mapped[int] = mapped_column(
        ForeignKey("evaluations.id"), nullable=False
    )
    inscription_id: Mapped[int] = mapped_column(
        ForeignKey("inscriptions.id"), nullable=False
    )
    note: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False)
    commentaire: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    evaluation: Mapped["Evaluation"] = relationship(
        back_populates="notes"
    )
    inscription: Mapped["Inscription"] = relationship(
        back_populates="notes"
    )


# 14. PRESENCES
class Presence(Base):
    __tablename__ = "presences"
    __table_args__ = (
        UniqueConstraint(
            "cours_id", "inscription_id",
            name="uq_presence_cours_inscription",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cours_id: Mapped[int] = mapped_column(
        ForeignKey("cours.id"), nullable=False
    )
    inscription_id: Mapped[int] = mapped_column(
        ForeignKey("inscriptions.id"), nullable=False
    )
    statut: Mapped[str] = mapped_column(String(30), nullable=False)
    justification: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    cours: Mapped["Cours"] = relationship(back_populates="presences")
    inscription: Mapped["Inscription"] = relationship(
        back_populates="presences"
    )
