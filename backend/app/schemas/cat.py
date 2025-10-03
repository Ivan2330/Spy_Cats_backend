from pydantic import BaseModel, conint, confloat

class CatBase(BaseModel):
    name: str
    years_experience: conint(ge=0, le=50)
    breed: str
    salary: confloat(ge=0)

class CatCreate(CatBase):
    pass

class CatUpdateSalary(BaseModel):
    salary: confloat(ge=0)

class CatOut(CatBase):
    id: int
    class Config:
        from_attributes = True
