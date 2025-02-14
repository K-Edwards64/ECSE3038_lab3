import fastapi
from datetime import datetime
from typing import List
from fastapi import FastAPI, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
from uuid import UUID, uuid4

app = FastAPI()

class Tank(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    location: str
    lat: float
    long: float

class Tank_Update(BaseModel):
    location: str | None = None
    lat: float | None = None
    long: float | None = None

list: List[Tank] = []

@app.get("/tank")
async def get_list():
    return list

@app.get("/tank/{id}")
async def get_spec_tank(id: UUID):
    for tank in list:
        if tank.id == id:
            return tank
    raise HTTPException(status_code=404, detail="Tank Not Found")

@app.post("/tank")
async def post_tank(tank_request: Tank):
    list.append(tank_request)
    tank_json = jsonable_encoder(tank_request)

    return tank_json

@app.delete("/tank/{id}")
async def delete_tank(id: UUID):
    for tank in list:
        if tank.id == id:
            list.remove(tank)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Tank Not Found")


@app.patch("/tank/{id}")
async def patch_tank(tank_update: Tank_Update ,id: UUID):
    for i, tank in enumerate(list):
        if tank.id == id:
            tank_update_list = tank_update.model_dump(exclude_unset=True)

            try:
                updated_tank = tank.copy(update=tank_update_list)
                list[i] = updated_tank

                json_updated_tank = jsonable_encoder(updated_tank)
                return JSONResponse(json_updated_tank, status_code=200)
            except ValidationError:
                raise HTTPException(status_code=400, detail="Tank must have a location, latitude coordinate or longitude coordinate")
        raise HTTPException(status_code=404, detail="Tank not found, could not update")
            
                 


