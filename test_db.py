
from sqlalchemy import text
from app.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT VERSION()"))
        version = result.scalar()

        print("Connexion à la base réussie !")
        print("Version du serveur :", version)

except Exception as erreur:
    print("Échec de la connexion à MySQL.")
    print("Erreur :", erreur)
