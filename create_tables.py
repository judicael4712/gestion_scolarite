
from app.database import Base, engine
from app import models

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    print("Tables créées avec succès !")
    print("Tables :", ", ".join(Base.metadata.tables.keys()))
