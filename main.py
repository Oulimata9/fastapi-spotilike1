# main.py
from fastapi import FastAPI, Depends , HTTPException
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Time, Date
from sqlalchemy.orm import Session
from fastapi_spotilike1.database import get_db
from fastapi_spotilike1.database import SessionLocal, engine
#from fastapi_spotilike1.models import Album, Artiste, Genre, Morceau, Utilisateur  # Import depuis le dossier app.models
from fastapi_spotilike1.crud import get_album

from sqlalchemy.orm import declarative_base
from typing import List
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from fastapi_spotilike1 import database, crud, models
from fastapi_spotilike1.database import Base


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
class SongBase(BaseModel):
    Titre: str
    Duree: str
    artisteID: int
    Genre_ID: int
    Album_ID: int

class SongResponse(SongBase):
    IDmorceau: int    
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
class GenreResponse(BaseModel):
    IDgenre: int
    Titre: str
    Description: str

class MorceauResponse(BaseModel):
    IDmorceau: int
    Titre: str
    Duree: str  # Vous pouvez ajuster le type en fonction de votre modèle de données
    artisteID: int
    Genre_ID: int
    Album_ID: int    

class UtilisateurBase(BaseModel):
    Nom_utilisateur: str
    Mot_de_passe: str
    Email: str

class UtilisateurCreate(UtilisateurBase):
    pass

class UtilisateurResponse(UtilisateurBase):
    IDutilisateur: int
    
        
# CRUD operations
# You can define functions like `create_album`, `get_album`, etc., using the SQLAlchemy session

# Endpoints
    
#1. GET - /api/albums : Récupère la liste de tous les albums    
@app.post("/api/albums", response_model=AlbumResponse)
async def create_album(album: AlbumCreate, db: Session = Depends(get_db)):
    # Implement your logic to create an album in the database
    pass

# 2. GET - /api/albums/:id : Récupère les détails de l’album précisé par :id

@app.get("/api/albums/{album_id}", response_model=AlbumResponse)
async def read_album(album_id: int, db: Session = Depends(get_db)):
    db_album = get_album(db, album_id)
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return db_album

#3. GET - /api/albums/:id/songs : Récupère les morceaux de l’album précisé par :id
@app.get("/api/albums/{album_id}/songs", response_model=List[SongResponse])
async def read_album_songs(album_id: int, db: Session = Depends(database.get_db)):
    db_album = crud.get_album(db, album_id)
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")

    songs = crud.get_songs_by_album(db, album_id)
    return songs

#4. GET - /api/genres : Récupère la liste de tous les genres
@app.get("/api/genres", response_model=List[GenreResponse])
async def get_genres(db: Session = Depends(database.get_db)):
    genres = crud.get_genres(db)
    return genres

#5. GET - /api/artists/:id/songs : Récupère la liste de tous les morceaux de l’artiste précisé par :id
@app.get("/api/artists/{artist_id}/songs", response_model=List[MorceauResponse])
async def get_artist_songs(artist_id: int, db: Session = Depends(database.get_db)):
    artist = crud.get_artiste(db, artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Artiste not found")

    songs = crud.get_songs_by_artist(db, artist_id)
    return songs

#6. POST - /api/users/signin : Ajout d’un utilisateur
@app.post("/api/users/signin", response_model=UtilisateurResponse)
async def create_user(user: UtilisateurCreate, db: Session = Depends(database.get_db)):
    db_user = crud.create_user(db, user)
    return db_user
#
#
#
#
#
#
#
#
#
#
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
