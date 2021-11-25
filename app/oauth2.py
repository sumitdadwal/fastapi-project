from base64 import decode
import re
from typing import AsyncContextManager
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from .config import settings


from fastapi.security import OAuth2PasswordBearer, oauth2

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#Algorithm
#Expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentails_exception):
 
    try: #because we can run into error at any line of code
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id") #to extract the data of user who tries to login

        if id is None:
            raise credentails_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentails_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Fuck off', headers={'WWW-Authenticate': 'Bearer'})


    token = verify_access_token(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

    
    #this fucntion will be user as dependency in fundtions or path operations that require logins. f
    #for example if a user needs to login to create a post this will be passed in as 
    #def create_post(post: -----, db: -----, get_curent_user: int = Depends(oauth2.get_current_user)):
    #this will make sure that user is sending a token.
    #then we return the verify_access_token function to verify that token.
    #if the token is valid user will be able to access create_post path.