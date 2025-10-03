from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.db import get_session
from app.models.mission import Mission
from app.models.target import Target
from app.models.cat import Cat
from app.schemas.mission import MissionCreate, MissionAssign, MissionOut
from app.schemas.target import TargetUpdate

router = APIRouter(prefix="/missions", tags=["missions"])

@router.post("", response_model=MissionOut, status_code=status.HTTP_201_CREATED)
async def create_mission(payload: MissionCreate, db: AsyncSession = Depends(get_session)):
    mission = Mission(complete=False)
    for t in payload.targets:
        mission.targets.append(Target(**t.model_dump()))
    db.add(mission)
    await db.commit()
    res = await db.execute(
        select(Mission)
        .options(selectinload(Mission.targets), selectinload(Mission.cat))
        .where(Mission.id == mission.id)
    )
    mission = res.scalar_one()
    return mission


@router.get("", response_model=list[MissionOut])
async def list_missions(db: AsyncSession = Depends(get_session)):
    res = await db.execute(
        select(Mission).options(selectinload(Mission.targets), selectinload(Mission.cat))
    )
    return res.scalars().unique().all()


@router.get("/{mission_id}", response_model=MissionOut)
async def get_mission(mission_id: int, db: AsyncSession = Depends(get_session)):
    res = await db.execute(
        select(Mission)
        .options(selectinload(Mission.targets), selectinload(Mission.cat))
        .where(Mission.id == mission_id)
    )
    m = res.scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Mission not found")
    return m


@router.patch("/{mission_id}/assign", response_model=MissionOut)
async def assign_cat(mission_id: int, payload: MissionAssign, db: AsyncSession = Depends(get_session)):
    m = await db.get(Mission, mission_id)
    if not m:
        raise HTTPException(404, "Mission not found")
    cat = await db.get(Cat, payload.cat_id)
    if not cat:
        raise HTTPException(404, "Cat not found")

    q = await db.execute(select(Mission).where(Mission.cat_id == cat.id, Mission.complete == False))
    if q.scalars().first():
        raise HTTPException(409, "Cat already has an active mission")

    m.cat_id = cat.id
    await db.commit()
    res = await db.execute(
        select(Mission)
        .options(selectinload(Mission.targets), selectinload(Mission.cat))
        .where(Mission.id == m.id)
    )
    return res.scalar_one()


@router.patch("/{mission_id}/targets/{target_id}", response_model=MissionOut)
async def update_target(mission_id: int, target_id: int, payload: TargetUpdate, db: AsyncSession = Depends(get_session)):
    m = await db.get(Mission, mission_id)
    if not m:
        raise HTTPException(404, "Mission not found")
    t = await db.get(Target, target_id)
    if not t or t.mission_id != m.id:
        raise HTTPException(404, "Target not found")

    if m.complete:
        raise HTTPException(409, "Mission is completed; targets are frozen")
    if t.complete and (payload.notes is not None):
        raise HTTPException(409, "Target is completed; notes are frozen")

    if payload.notes is not None:
        t.notes = payload.notes
    if payload.complete is not None:
        t.complete = payload.complete

    if all(tt.complete for tt in m.targets):
        m.complete = True

    await db.commit()
    res = await db.execute(
        select(Mission)
        .options(selectinload(Mission.targets), selectinload(Mission.cat))
        .where(Mission.id == m.id)
    )
    return res.scalar_one()