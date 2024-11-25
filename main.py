from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.teams import router as team_router

app = FastAPI(
    title="My SLMS FastAPI Application",
    description="This is an application for Sports and League MIS RESTFUL APIS", 
    version="1.0.0" 
)

@app.get("/")
def greet():
    return {"message": "Hello, Fast People!"}
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(team_router, prefix="/auth", tags=["Teams"])
