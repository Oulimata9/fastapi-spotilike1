# fastapi-spotilike1
Projet FastAPI Spotilike
pip install python-jose
(venv) PS C:\cours b3\fastapi-spotilike1> pip list
>>
Package           Version
----------------- ----------
annotated-types   0.6.0
anyio             3.7.1
asgiref           3.7.2
certifi           2023.11.17
click             8.1.7
colorama          0.4.6
distlib           0.3.8
ecdsa             0.18.0
fastapi           0.109.0
filelock          3.13.1
greenlet          3.0.3
h11               0.14.0
idna              3.6
pip               23.2.1
pipenv            2023.11.17
platformdirs      4.1.0
pyasn1            0.5.1
pydantic          1.10.14
pydantic_core     2.16.1
PyJWT             1.7.1
python-decouple   3.3
python-jose       3.3.0
rsa               4.9
setuptools        69.0.3
six               1.16.0
sniffio           1.3.0
SQLAlchemy        2.0.25
starlette         0.35.1
typing_extensions 4.9.0
uvicorn           0.15.0
virtualenv        20.25.0

## Description
Spotilike est une API FastAPI qui gère des informations sur les albums, les artistes et les morceaux. Elle permet aux utilisateurs de récupérer des détails sur les albums, d'ajouter de nouveaux albums, et bien plus encore.

## Installation
1. Clonez ce dépôt.
2. Installez les dépendances avec la commande : `pip install -r requirements.txt`
3. Démarrez l'application avec : `uvicorn main:app --reload`

## Configuration
- Assurez-vous de définir la clé secrète dans le fichier `main.py` pour la génération de tokens JWT.
- Configurez les paramètres de la base de données dans le fichier `database.py`.

## Utilisation
 Accédez à l'API en ouvrant un navigateur et en allant à http://127.0.0.1:8000/docs#/

## Structure du Projet
- `main.py`: Point d'entrée de l'application.
- `database.py`: Configuration de la base de données.
- `crud.py`: Opérations CRUD sur la base de données.
- `models.py`: Définition des modèles SQLAlchemy.
- `security.py`: Fonctions de sécurité et gestion des tokens JWT.
- `requirements.txt`: Liste des dépendances Python.

## Auteurs
- Diedhiou Oulimata - oulishudiedhiou03@gmail.com

##
##
##
##
##