from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

from app.database import Base
    


class PostBase(BaseModel): #
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel): #needs to be created after schemas.
    Post: PostResponse
    votes: int
    

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)




class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None


