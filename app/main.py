from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from app.data import get_db, init_db
from app.models import Station
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

init_db()

app = FastAPI()

@app.get("/health")
def health():
    return {"status" : "ok"}

class stationCreate(BaseModel) :
    name : str
    ville : str
    code : str
    status : str


@app.post("/stations", status_code=status.HTTP_201_CREATED)
def create_station(station: stationCreate, db: Session = Depends(get_db)):
    new = Station(
        code=station.code,
        name=station.name,
        ville=station.ville,
        status=station.status
    )
    db.add(new)
    try:
        db.commit()
        db.refresh(new)
        return new
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Code déjà utilisé")

    
@app.get("/stations")
def get_stations(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Station)
    if status is not None:
        query = query.filter(Station.status == status)
    return query.all()


@app.get("/stations/{id}")
def get_station(id: int, db: Session = Depends(get_db)):
    station = db.query(Station).filter(Station.id == id).first()
    if station is None:
        raise HTTPException(status_code=404, detail="Station non trouvée")
    return station


class StationPatch(BaseModel):
    name: str | None = None
    status: str | None = None


@app.patch("/stations/{id}")
def patch_station(id: int, patch: StationPatch, db: Session = Depends(get_db)):
    station = db.query(Station).filter(Station.id == id).first()
    if station is None:
        raise HTTPException(status_code=404, detail="Station non trouvée")
    if patch.name is not None:
        station.name = patch.name
    if patch.status is not None:
        station.status = patch.status
    db.commit()
    db.refresh(station)
    return station