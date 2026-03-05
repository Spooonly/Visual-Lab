import json
from fastapi import FastAPI
from sqlalchemy.orm import Session

from .db import engine, SessionLocal
from .models import Base, Experiment
from .schemas import MixRequest
from .chemistry.engine import simulate_mix

app = FastAPI(title="Virtual Lab")

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/simulate/mix")
def mix(req: MixRequest):
    result = simulate_mix(req.reagents)

    # save to DB
    db: Session = SessionLocal()
    try:
        exp = Experiment(
            reagents=json.dumps(req.reagents, ensure_ascii=False),
            result=json.dumps(result, ensure_ascii=False),
        )
        db.add(exp)
        db.commit()
        db.refresh(exp)
    finally:
        db.close()

    return {"experiment_id": exp.id, "result": result}
