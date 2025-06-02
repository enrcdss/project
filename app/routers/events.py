from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select
from models.event import Event
from data.db import SessionDep

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/")
def get_events(session: SessionDep) -> list[Event]:
    return session.exec(select(Event)).all()

@router.post("/")
def create_event(event: Event, session: SessionDep) -> Event:
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

@router.get("/{id}")
def get_event(id: int = Path(..., description="ID of the event"), session: SessionDep = None) -> Event:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{id}")
def update_event(
    id: int,
    new_event: Event,
    session: SessionDep
):
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.title = new_event.title
    event.description = new_event.description
    event.date = new_event.date
    event.location = new_event.location

    session.add(event)
    session.commit()
    return event

@router.delete("/{id}")
def delete_event(id: int, session: SessionDep):
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(event)
    session.commit()
    return {"detail": "Event deleted"}

@router.delete("/")
def delete_all_events(session: SessionDep):
    session.exec(select(Event).delete())
    session.commit()
    return {"detail": "All events deleted"}
