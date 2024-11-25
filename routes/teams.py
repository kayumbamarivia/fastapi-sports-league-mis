import json
from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from config.security import get_current_user
from dto.responses import TeamResponse, SucessResponse, TeamCreate
from config.database import get_db, Base, engine
from models.teams import Teams

router = APIRouter()

NOT_FOUND = "Team not found" 


Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]
current_user = Annotated[str, Depends(get_current_user)]

@router.post("/teams/create", response_model=SucessResponse)
async def create_team(team: TeamCreate, db: db_dependency, current_user: current_user):
    db_team = db.query(Teams).filter(Teams.name == team.name).first()
    if db_team:
        raise HTTPException(status_code=400, detail="Team already there")
    new_team = Teams(name=team.name, coach=team.coach, players=team.players)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return SucessResponse(message="Team created sucessfully!")


@router.get("/teams", response_model=List[TeamResponse])
async def get_teams(db: db_dependency, current_user: current_user):
    db_teams = db.query(Teams).all()
    return [
        TeamResponse(
            id=t.id,
            name=t.name,
            coach=t.coach,
            players=json.loads(t.players) if isinstance(t.players, str) else t.players
            )
        for t in db_teams
        ]

@router.get("/teams/{t_id}", response_model=TeamResponse)
async def get_team_by_id(t_id: int, db: db_dependency, current_user: current_user):
    db_team = db.query(Teams).filter(Teams.id==t_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return TeamResponse(
            id=db_team.id,
            name=db_team.name,
            coach=db_team.coach,
            players=json.loads(db_team.players) if isinstance(db_team.players, str) else db_team.players
            )
    
@router.put("/teams/{t_id}/edit", response_model=SucessResponse)
async def update_team_by_id(t_id: int, t: TeamCreate, db: db_dependency, current_user: current_user):
    db_team = db.query(Teams).filter(Teams.id==t_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    
    db_team.name = t.name
    db_team.coach = t.coach
    db_team.players = t.players
    db.commit()
    db.refresh(db_team)
    return SucessResponse(message="Team updated successfully!")
    
@router.delete("/teams/{u_id}/delete", response_model=SucessResponse)
async def delete_team_by_id(t_id: int, db: db_dependency, current_user: current_user):
    db_team = db.query(Teams).filter(Teams.id==t_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    db.delete(db_team)
    db.commit()
    
    return SucessResponse(message="Team deleted successfully!")

@router.delete("/teams/delete_all")
async def delete_all_teams(db: db_dependency, current_user: current_user):
    try:
        db.query(Teams).delete()
        db.commit()
        return SucessResponse(message="All Teams have been deleted successfully.")
    except Exception as e:
        print(e)
        db.rollback() 
        raise HTTPException(status_code=500, detail="An error occurred while deleting Teams.")
