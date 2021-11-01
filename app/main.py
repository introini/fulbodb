import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, AnyHttpUrl
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio
from dotenv import load_dotenv
from app.database import models

load_dotenv()

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client.fulbodb

@app.post("/", response_description="Add new team", response_model=models.TeamModel)
async def create_team(team: models.TeamModel = Body(...)):
    team = jsonable_encoder(team)
    new_team = await db["teams"].insert_one(team)
    created_team = await db["teams"].find_one({"_id": new_team.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_team)


@app.get(
    "/", response_description="List all teams", response_model=List[models.TeamModel]
)
async def list_teams():
    teams = await db["teams"].find().to_list(1000)
    return teams


@app.get(
    "/by-id/{id}", response_description="Get a single team by id", response_model=models.TeamModel
)
async def show_team(id: str):
    if (team := await db["teams"].find_one({"_id": id})) is not None:
        return team

    raise HTTPException(status_code=404, detail=f"team {id} not found")

@app.get(
    "/teams/{slug}", response_description="Get a single team by slug", response_model=models.TeamModel
)
async def show_team(slug: str):
    if (team := await db["teams"].find_one({"slug": slug})) is not None:
        return team

    raise HTTPException(status_code=404, detail=f"team {slug} not found")


@app.put("/{id}", response_description="Update a team", response_model=models.TeamModel)
async def update_team(id: str, team: models.UpdateTeamModel = Body(...)):
    team = {k: v for k, v in team.dict().items() if v is not None}

    if len(team) >= 1:
        update_result = await db["teams"].update_one({"_id": id}, {"$set": team})

        if update_result.modified_count == 1:
            if (
                updated_team := await db["teams"].find_one({"_id": id})
            ) is not None:
                return updated_team

    if (existing_team := await db["teams"].find_one({"_id": id})) is not None:
        return existing_team

    raise HTTPException(status_code=404, detail=f"team {id} not found")


@app.delete("/{id}", response_description="Delete a team")
async def delete_team(id: str):
    delete_result = await db["teams"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"team {id} not found")
