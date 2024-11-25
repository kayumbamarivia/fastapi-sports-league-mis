from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from config.security import get_current_user
from dto.responses import Login, Token, UserCreate, SucessResponse, UserResponse
from utils.auth import decode_access_token, hash_password, verify_password, create_access_token
from config.database import get_db, Base, engine
from models.users import Users

router = APIRouter()

NOT_FOUND = "User not found" 


Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]
current_user = Annotated[str, Depends(get_current_user)]

@router.post("/register", response_model=SucessResponse)
async def register(user: UserCreate, db: db_dependency):
    db_user = db.query(Users).filter(Users.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = Users(name=user.name, email=user.email, hashed_password=hash_password(user.password), role=user.role, image_url=str(user.image_url))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return SucessResponse(message="User created sucessfully!")

@router.post("/login", response_model=Token)
async def login(user: Login, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/users", response_model=List[UserResponse])
async def get_users(db: db_dependency, current_user: current_user):
    db_users = db.query(Users).all()
    return [
        UserResponse(
            id=u.id,
            name=u.name,
            email=u.email,
            role=u.role,
            image_url=u.image_url
            )
        for u in db_users
        ]

@router.get("/users/{u_id}", response_model=UserResponse)
async def get_user_by_id(u_id: int, db: db_dependency, current_user: current_user):
    db_user = db.query(Users).filter(Users.id==u_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return UserResponse(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            role=db_user.role,
            image_url=db_user.image_url
        )
    
@router.put("/users/{u_id}/edit", response_model=SucessResponse)
async def update_user_by_id(u_id: int, u: UserCreate, db: db_dependency, current_user: current_user):
    db_user = db.query(Users).filter(Users.id==u_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    
    db_user.name = u.name
    db_user.email = u.email
    db_user.hashed_password = hash_password(u.password)
    db_user.role = u.role
    db_user.image_url = str(u.image_url)
    db.commit()
    db.refresh(db_user)
    return SucessResponse(message="User updated successfully!")
    
@router.delete("/users/{u_id}/delete", response_model=SucessResponse)
async def delete_user_by_id(u_id: int, db: db_dependency, current_user: current_user):
    db_user = db.query(Users).filter(Users.id==u_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    db.delete(db_user)
    db.commit()
    
    return SucessResponse(message="User deleted successfully!")

@router.delete("/users/delete_all")
async def delete_all_users(db: db_dependency, current_user: current_user):
    try:
        db.query(Users).delete()
        db.commit()
        return SucessResponse(message="All Users have been deleted successfully.")
    except Exception as e:
        print(e)
        db.rollback() 
        raise HTTPException(status_code=500, detail="An error occurred while deleting users.")
