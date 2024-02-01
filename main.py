# main.py
from fastapi import FastAPI, Depends , HTTPException
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Time, Date
from sqlalchemy.orm import Session
from fastapi_spotilike1.database import get_db, SessionLocal, engine 
from fastapi_spotilike1.crud import get_album, get_user_by_username
from fastapi_spotilike1.models import Morceau
from fastapi_spotilike1.models import Artiste
from fastapi_spotilike1.security import verify_password
from sqlalchemy.orm import declarative_base
from typing import List
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_spotilike1 import database, crud, models, token
from fastapi_spotilike1.database import Base
from datetime import timedelta, datetime
from jose import jwt
from fastapi.exceptions import HTTPException
from fastapi_spotilike1.crud import MorceauCreate 
from fastapi_spotilike1.models import ArtisteResponse
from fastapi_spotilike1.models import GenreResponse
from passlib.context import CryptContext

# FastAPI app
app = FastAPI()

# OAuth2PasswordBearer for authentication (you may modify this)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define your SQLAlchemy models
Base = declarative_base()

# Clé secrète pour signer le token (à remplacer par votre propre clé secrète)
secret = "ea504dfd74cdc3fbddcb4e67c73b6070"
ALGORITHM = "HS256"

# Create the database tables
Base.metadata.create_all(bind=engine)
# Définition de la fonction get_token_header
def get_token_header(x_token: str = Depends(oauth2_scheme)):
    return x_token
app = FastAPI(dependencies=[Depends(get_token_header)])


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


# Pydantic 
class Token(BaseModel):
    access_token: str
    token_type: str
        
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

class AlbumResponse(BaseModel):
    IDalbum: int
    Titre: str
    Pochette: str
    Date_sortie: str
    liste_morceaux: str
    Artiste_ID: int


# Endpoints
    
#1. GET - /api/albums : Récupère la liste de tous les albums    
@app.post("/api/albums", response_model=AlbumResponse)
async def create_album(album: AlbumCreate, db: Session = Depends(get_db)):
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

#7. POST - /api/users/login : Connexion d’un utilisateur (JWT)
# Fonction pour créer un token JWT
def create_jwt_token(username: str) -> str:
    expiration = datetime.utcnow() + timedelta(hours=1)  # Définissez la durée de validité du token
    token_data = {"sub": username, "exp": expiration}
    token = jwt.encode(token_data, "secret", algorithm="HS256")
    return token
def get_user_by_username(db: Session, username: str):
    return db.query(Utilisateur).filter(Utilisateur.Nom_utilisateur == username).first()
def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user or not verify_password(password, user["password"]):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme)):
    pass
@app.post("/api/users/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        ) 
    # Créer et retourner le token JWT
    token = create_jwt_token(user.username)
    return {"access_token": token, "token_type": "bearer"}

#8. POST - /api/albums : Ajout d’un album
@app.post("/api/albums", response_model=models.AlbumCreate)
async def create_album(album: crud.AlbumCreate, db: Session = Depends(database.get_db)):
    return crud.create_album(db=db, album=album)

#9. POST - /api/albums/:id/songs : Ajout d’un morceau dans l’album précisé par :id
@app.post("/api/albums/{album_id}/songs", response_model=None)  #models.Morceau, response_model_exclude_unset=True)
async def create_song_for_album(
    album_id: int, song: crud.MorceauCreate, db: Session = Depends(database.get_db)
):
    return crud.create_song_for_album(db=db, album_id=album_id, song=song)

#10. PUT - /api/artists/:id : Modification de l’artiste précisé par :id
@app.put("/api/artists/{artist_id}", response_model=None) #models.Artiste)
async def update_artist(
    artist_id: int, updated_artist: crud.ArtisteUpdate, db: Session = Depends(database.get_db)
):
    db_artist = crud.update_artist(db=db, artist_id=artist_id, updated_artist=updated_artist)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artiste not found")
    return db_artist

#11. PUT - /api/albums/:id : Modification de l’album précisé par :id
@app.put("/api/albums/{album_id}", response_model=models.AlbumResponse)
async def update_album(
    album_id: int, updated_album: models.AlbumUpdate, db: Session = Depends(database.get_db)
):
    db_album = crud.update_album(db=db, album_id=album_id, updated_album=updated_album)
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return db_album

#12. PUT - /api/genres/:id : Modification du genre précisé par :id
@app.put("/api/genres/{genre_id}", response_model=models.GenreResponse)
async def update_genre(
    genre_id: int, updated_genre: models.GenreUpdate, db: Session = Depends(database.get_db)
):
    db_genre = crud.update_genre(db=db, genre_id=genre_id, updated_genre=updated_genre)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre

#13. DELETE - /api/users/:id : Suppression de utilisateur précisé par :id
@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user_related_items(db, user_id)

    # Supprimer l'utilisateur
    db_user = crud.delete_user(db, user_id)
    return {"message": "User deleted successfully"}


#14. DELETE - /api/albums/:id : Suppression de l’album précisé par :id
async def delete_album(album_id: int, db: Session = Depends(database.get_db)):
    db_album = crud.get_album(db, album_id)
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    # Supprimer les morceaux liés à cet album
    crud.delete_songs_by_album(db, album_id)
    # Supprimer l'album lui-même
    deleted_album = crud.delete_album(db, album_id)
    return deleted_album

#15. DELETE - /api/artists/:id : Supression de l’artiste précisé par :id
@app.delete("/api/artists/{artist_id}", response_model=models.ArtisteResponse)
async def delete_artist(artist_id: int, db: Session = Depends(database.get_db)):
    # Vérifier si l'artiste existe
    db_artist = crud.get_artist(db, artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")

    # Supprimer tous les morceaux associés à cet artiste
    crud.delete_songs_by_artist(db, artist_id)

    # Supprimer l'artiste lui-même (avec suppression en cascade)
    deleted_artist = crud.delete_artist(db, artist_id)

    return deleted_artist
#
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
