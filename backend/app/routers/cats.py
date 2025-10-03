from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_session
from app.models.cat import Cat
from app.schemas.cat import CatCreate, CatOut, CatUpdateSalary
from app.services.cat_breeds import validate_breed

router = APIRouter(prefix="/cats", tags=["cats"])

@router.post("", response_model=CatOut, status_code=status.HTTP_201_CREATED)
async def create_cat(payload: CatCreate, db: AsyncSession = Depends(get_session)):
    ok = await validate_breed(payload.breed)
    if not ok:
        raise HTTPException(status_code=422, detail="Invalid breed (TheCatAPI validation failed)")

    cat = Cat(**payload.model_dump())
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat

@router.get("", response_model=list[CatOut])
async def list_cats(db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(Cat))
    return list(res.scalars().all())

@router.get("/{cat_id}", response_model=CatOut)
async def get_cat(cat_id: int, db: AsyncSession = Depends(get_session)):
    obj = await db.get(Cat, cat_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Cat not found")
    return obj

@router.patch("/{cat_id}", response_model=CatOut)
async def update_salary(cat_id: int, payload: CatUpdateSalary, db: AsyncSession = Depends(get_session)):
    obj = await db.get(Cat, cat_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Cat not found")
    obj.salary = float(payload.salary)
    await db.commit()
    await db.refresh(obj)
    return obj

@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cat(cat_id: int, db: AsyncSession = Depends(get_session)):
    obj = await db.get(Cat, cat_id)
    if not obj:
        return
    await db.delete(obj)
    await db.commit()
