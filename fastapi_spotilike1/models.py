from sqlalchemy import Column, Integer, String, ForeignKey, Text, Time, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from .database import Base
from pydantic import BaseModel

Base = declarative_base()

class Album(Base):
    __tablename__ = "album"
    IDalbum = Column(Integer, primary_key=True, index=True)
    Titre = Column(String, index=True)
    Pochette = Column(String)
    Date_sortie = Column(Date)
    liste_morceaux = Column(String)
    Artiste_ID = Column(Integer, ForeignKey("artiste.IDartiste"))

class Artiste(Base):
    __tablename__ = "artiste"
    IDartiste = Column(Integer, primary_key=True, index=True)
    Nom_artiste = Column(String, index=True)
    Avatar = Column(String)
    Biographie = Column(Text)

class UtilisateurCreate(BaseModel):
    # Définissez les champs de votre modèle UtilisateurCreate
    Nom_utilisateur: str
    Mot_de_passe: str
    Email: str
# Ajoutez d'autres modèles selon vos besoins
