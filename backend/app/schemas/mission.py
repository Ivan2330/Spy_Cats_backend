from pydantic import BaseModel, conlist
from app.schemas.target import TargetCreate, TargetOut

class MissionCreate(BaseModel):
    targets: conlist(TargetCreate, min_length=1, max_length=3)

class MissionAssign(BaseModel):
    cat_id: int

class MissionOut(BaseModel):
    id: int
    cat_id: int | None
    complete: bool
    targets: list[TargetOut]
    class Config:
        from_attributes = True
