from typing import List
from pydantic import BaseModel, EmailStr, HttpUrl

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    image_url: HttpUrl
    
class Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    

class UserResponse(BaseModel): 
    id: int | None=None
    name: str
    email: EmailStr
    role: str
    image_url: HttpUrl | None=None
    
    class Config:
        orm_mode = True
    
class SucessResponse(BaseModel):
    message: str

class TeamCreate(BaseModel):
    name: str
    coach: str
    players: List[str]
    
class TeamResponse(BaseModel):
    id: int | None=None
    name: str
    coach: str
    players: List[str]
    
    class Config:
        orm_mode = True