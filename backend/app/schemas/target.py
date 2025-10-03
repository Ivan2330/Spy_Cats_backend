from pydantic import BaseModel

class TargetCreate(BaseModel):
    name: str
    country: str
    notes: str = ""
    complete: bool = False

class TargetUpdate(BaseModel):
    notes: str | None = None
    complete: bool | None = None

class TargetOut(TargetCreate):
    id: int
    class Config:
        from_attributes = True
