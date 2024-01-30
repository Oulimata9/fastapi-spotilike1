# main.py
from fastapi import FastAPI, Depends # , HTTPException
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Time, Date
from sqlalchemy.orm import declarative_base
from typing import List
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from .database import Base
from .crud import create_album, get_db
from fastapi_spotilike1 import crud, models, database 

# FastAPI app
app = FastAPI()

# OAuth2PasswordBearer for authentication (you may modify this)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define your SQLAlchemy models
Base = declarative_base()

# Create the database tables
Base.metadata.create_all(bind=engine)

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

class Genre(Base):
    __tablename__ = "genre"
    IDgenre = Column(Integer, primary_key=True, index=True)
    Titre = Column(String, index=True)
    Description = Column(Text)

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


# Pydantic models for data validation
class AlbumBase(BaseModel):
    Titre: str
    Pochette: str
    Date_sortie: str
    liste_morceaux: str
    Artiste_ID: int

class AlbumCreate(AlbumBase):
    pass

class AlbumResponse(AlbumBase):
    IDalbum: int

class ArtisteBase(BaseModel):
    Nom_artiste: str
    Avatar: str
    Biographie: str

class ArtisteCreate(ArtisteBase):
    pass

class ArtisteResponse(ArtisteBase):
    IDartiste: int

# CRUD operations
# You can define functions like `create_album`, `get_album`, etc., using the SQLAlchemy session

# Endpoints
@app.post("/api/albums", response_model=AlbumResponse)
async def create_album(album: AlbumCreate, db: Session = Depends(get_db)):
    # Implement your logic to create an album in the database
    pass

# Implement other endpoints similarly...

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
