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


class Morceau(Base):
    __tablename__ = "morceau"
    IDmorceau = Column(Integer, primary_key=True, index=True)
    Titre = Column(String, index=True)
    Duree = Column(Time)
    artisteID = Column(Integer, ForeignKey("artiste.IDartiste"))
    Genre_ID = Column(Integer, ForeignKey("genre.IDgenre"))
    Album_ID = Column(Integer, ForeignKey("album.IDalbum"))        

class Utilisateur(Base):
    __tablename__ = "utilisateur"
    
    IDutilisateur = Column(Integer, primary_key=True, index=True)
    Nom_utilisateur = Column(String, index=True)
    Mot_de_passe = Column(String)
    Email = Column(String, index=True)

class Genre(Base):
    __tablename__ = "genre"
    IDgenre = Column(Integer, primary_key=True)
    Titre = Column(String, nullable=False)


class UtilisateurCreate(BaseModel):
    # Définissez les champs de votre modèle UtilisateurCreate
    Nom_utilisateur: str
    Mot_de_passe: str
    Email: str


class AlbumResponse(BaseModel):
    IDalbum: int
    Titre: str
    Pochette: str
    Date_sortie: str
    liste_morceaux: str
    Artiste_ID: int

    class Config:
        from_attributes = True
#pydantic
# Modèle Pydantic pour la création d'un album
class AlbumCreate(BaseModel):
    Titre: str
    Pochette: str
    Date_sortie: str
    liste_morceaux: str
    Artiste_ID: int

# Modèle Pydantic pour la création d'un morceau
class MorceauCreate(BaseModel):
    Titre: str
    Duree: str
    artisteID: int
    Genre_ID: int
    Album_ID: int

    class Config:
        orm_mode = True


# Modèle Pydantic pour la mise à jour d'un artiste
class ArtisteBase(BaseModel):
    Nom_artiste: str
    Avatar: str
    Biographie: str

class ArtisteCreate(ArtisteBase):
    pass

class ArtisteResponse(ArtisteBase):
    IDartiste: int
    Nom_artiste: str
    Avatar: str
    Biographie: str

class ArtisteUpdate(BaseModel):
    Nom_artiste: str
    Avatar: str
    Biographie: str


class AlbumUpdate(BaseModel):
    Titre: str
    Pochette: str
    Date_sortie: str
    liste_morceaux: str
    Artiste_ID: int

class GenreUpdate(BaseModel):
    Titre: str
    Description: str    
   
class GenreResponse(BaseModel):
    IDgenre: int
    Titre: str
    Description: str    