
from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Formation(Base):
    __tablename__ = "formations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    nom: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    duree_mois: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    actif: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
