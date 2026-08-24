from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Change
from ..schemas import ChangeCreate, ChangeResponse

router = APIRouter(prefix="/changes", tags=["changes"])


@router.post("", response_model=ChangeResponse, status_code=status.HTTP_201_CREATED)
def create_change(payload: ChangeCreate, db: Session = Depends(get_db)):
    change = Change(**payload.model_dump())
    db.add(change)
    db.commit()
    db.refresh(change)
    return change


@router.get("", response_model=list[ChangeResponse])
def list_changes(db: Session = Depends(get_db)):
    statement = select(Change).order_by(Change.created_at.desc())
    return list(db.scalars(statement))


@router.get("/{change_id}", response_model=ChangeResponse)
def get_change(change_id: int, db: Session = Depends(get_db)):
    change = db.get(Change, change_id)
    if change is None:
        raise HTTPException(status_code=404, detail="Change not found")
    return change


@router.put("/{change_id}", response_model=ChangeResponse)
def update_change(change_id: int, payload: ChangeCreate, db: Session = Depends(get_db)):
    change = db.get(Change, change_id)
    if change is None:
        raise HTTPException(status_code=404, detail="Change not found")

    for field, value in payload.model_dump().items():
        setattr(change, field, value)

    db.commit()
    db.refresh(change)
    return change


@router.delete("/{change_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_change(change_id: int, db: Session = Depends(get_db)):
    change = db.get(Change, change_id)
    if change is None:
        raise HTTPException(status_code=404, detail="Change not found")

    db.delete(change)
    db.commit()
