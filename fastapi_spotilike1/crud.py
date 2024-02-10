from sqlalchemy.orm import Session
from . import models
from .models import UtilisateurCreate
from .models import AlbumCreate
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from .models import Utilisateur, Morceau
from fastapi_spotilike1.models import Album
from datetime import datetime


class MorceauCreate(BaseModel):
    Titre: str
    Duree: str
    artisteID: int
    Genre_ID: int
    Album_ID: int

# Modèle Pydantic pour la mise à jour d'un artiste
class ArtisteUpdate(BaseModel):
    Nom_artiste: Optional[str] = None
    Avatar: Optional[str] = None
    Biographie: Optional[str] = None

#2. Opérations CRUD pour la table "Album"
def get_album(db: Session, album_id: int):
    return db.query(models.Album).filter(models.Album.IDalbum == album_id).first()
def get_albums(db: Session):
    return db.query(models.Album).all()


#3. Fonction CRUD pour la table "Morceau"
def get_songs_by_album(db: Session, album_id: int):
    return db.query(models.Morceau).filter(models.Morceau.Album_ID == album_id).all()


#db.query(models.Morceau).filter(models.Morceau.IDalbum == album_id).all()

#4. Récupère la liste de tous les genres
def get_genres(db: Session):
    return db.query(models.Genre).all()

#5. Récupère la liste de tous les morceaux de l’artiste précisé par :id
def get_songs_by_artist(db: Session, artist_id: int):
    return db.query(models.Morceau).filter(models.Morceau.artisteID == artist_id).all()

def get_artiste(db: Session, artist_id: int):
    """
    Récupère un artiste par son ID.
    
    Args:
    - db: Session SQLAlchemy
    - artist_id: ID de l'artiste à récupérer
    
    Returns:
    - L'artiste récupéré ou None s'il n'existe pas
    """
    return db.query(models.Artiste).filter(models.Artiste.IDartiste == artist_id).first()

def create_user(db: Session, user: models.UtilisateurCreate):
    db_user = models.Utilisateur(Nom_utilisateur=user.Nom_utilisateur, Mot_de_passe=user.Mot_de_passe, Email=user.Email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#7. Connexion d’un utilisateur (JWT)
#def authenticate_user(db: Session, username: str, password: str):
 #   user = db.query(models.Utilisateur).filter(models.Utilisateur.Nom_utilisateur == username).first()
  #  if user and user.Mot_de_passe == password:
   #     return user
    #return None

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


#8. Opération CRUD pour l'ajout d'un album
# Fonction pour ajouter un album dans la base de données
def create_album(db: Session, album: models.AlbumCreate):
    # Convertir la chaîne de date en objet de date Python
    date_sortie = datetime.strptime(album.Date_sortie, "%Y-%m-%d").date()

    # Créer l'objet Album avec la date convertie
    db_album = Album(
        Titre=album.Titre,
        Pochette=album.Pochette,
        Date_sortie=date_sortie,
        liste_morceaux=album.liste_morceaux,
        Artiste_ID=album.Artiste_ID
    )

    # Ajouter l'objet Album à la session et le sauvegarder dans la base de données
    db.add(db_album)
    db.commit()
    db.refresh(db_album)

    return db_album

#9. Fonction pour ajouter un morceau à un album dans la base de données
def create_song_for_album(db: Session, album_id: int, song: models.MorceauCreate):
    new_song = models.Morceau(
        Titre=song.Titre,
        Duree=song.Duree,
        artisteID=song.artisteID,
        Genre_ID=song.Genre_ID,
        Album_ID=album_id
    )
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song


#10. Fonction pour mettre à jour un artiste dans la base de données
def update_artist(db: Session, artist_id: int, updated_artist: models.ArtisteUpdate):
    db_artist = db.query(models.Artiste).filter(models.Artiste.IDartiste == artist_id).first()
    if db_artist:
        for key, value in updated_artist.dict().items():
            setattr(db_artist, key, value)
        db.commit()
        db.refresh(db_artist)
    return db_artist

#11. Ajouter cette fonction pour mettre à jour un album
def update_album(db: Session, album_id: int, updated_album: models.AlbumUpdate):
    db_album = db.query(models.Album).filter(models.Album.IDalbum == album_id).first()
    if db_album:
        for key, value in updated_album.dict().items():
            setattr(db_album, key, value)
        db.commit()
        db.refresh(db_album)
    return db_album

#12. Ajouter cette fonction pour mettre à jour un genre
def update_genre(db: Session, genre_id: int, updated_genre: models.GenreUpdate):
    db_genre = db.query(models.Genre).filter(models.Genre.IDgenre == genre_id).first()
    if db_genre:
        for key, value in updated_genre.dict().items():
            setattr(db_genre, key, value)
        db.commit()
        db.refresh(db_genre)
    return db_genre

#13. Suppression de utilisateur précisé par :id
def delete_songs_by_user(db: Session, user_id: int):
    user = db.query(Utilisateur).filter(Utilisateur.IDutilisateur == user_id).first() 
    if user:
        # Supprimez les morceaux associés à cet utilisateur
        db.query(Morceau).filter(Morceau.artisteID == user.IDutilisateur).delete(synchronize_session='fetch')
        db.commit()

#14.  suppression d'un album
def delete_songs_by_album(db: Session, album_id: int):
    # Supprimer les morceaux associés à l'album
    db.query(models.Morceau).filter(models.Morceau.Album_ID == album_id).delete()
    db.commit()

def delete_album(db: Session, album_id: int):
    # Supprimer l'album
    db_album = db.query(models.Album).filter(models.Album.IDalbum == album_id).first()
    if db_album:
        # Supprimer les morceaux associés à l'album
        delete_songs_by_album(db, album_id)
        db.delete(db_album)
        db.commit()
        return db_album
    return None

#15. Supression de l’artiste précisé par :id
def delete_songs_by_artist(db: Session, artist_id: int):
    db.query(models.Morceau).filter(models.Morceau.artisteID == artist_id).delete()
    db.commit()

# Fonction pour supprimer un artiste avec suppression en cascade
def delete_artist(db: Session, artist_id: int):
    db_artist = db.query(models.Artiste).filter(models.Artiste.IDartiste == artist_id).first()
    if db_artist:
        # Supprimer l'artiste
        db.delete(db_artist)
        db.commit()
    return db_artist