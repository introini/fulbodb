from typing import Optional
from pydantic import BaseModel, Field, AnyHttpUrl
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class TeamModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    abbrev: str = Field(...)
    slug: str = Field(...)
    crest: Optional[AnyHttpUrl] = Field(...)
    colors: Optional[list] = Field(...)
    espn_url: Optional[AnyHttpUrl] = Field(...)
    forza_url: Optional[AnyHttpUrl] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "River Plate",
                "abbrev": "RIV",
                "slug": "river-plate",
                "crest": "https://localhost:8082/crests/river-plate.png",
                "colors": [243,1,1],
                "espn_url": "https://www.espn.com.ar/futbol/equipo/_/id/16/river-plate",
                "forza_url": "https://forzafootball.com/es/team/river-plate-3182",
            }
        }


class UpdateTeamModel(BaseModel):
    name: Optional[str]
    abbrev: Optional[str]
    slug: Optional[str]
    crest: Optional[AnyHttpUrl]
    colors: Optional[list]
    espn_url: Optional[AnyHttpUrl]
    forza_url: Optional[AnyHttpUrl]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "River Plate",
                "abbrev": "RIV",
                "slug": "river-plate",
                "crest": "http://localhost:8082/crests/river-plate.png",
                "colors": [243,1,1],
                "espn_url": "https://www.espn.com.ar/futbol/equipo/_/id/16/river-plate",
                "forza_url": "https://forzafootball.com/es/team/river-plate-3182",
            }
        }
