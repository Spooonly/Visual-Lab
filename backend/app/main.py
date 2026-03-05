import json
from typing import List
from sqlalchemy import desc
from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pathlib import Path


from .db import engine, SessionLocal
from .models import Base, Experiment
from .schemas import MixRequest
from .chemistry.engine import simulate_mix
from .chemistry.data_loader import load_reagents

app = FastAPI(title="Virtual Lab")

BASE_DIR = Path(__file__).resolve().parent

# Force-create folders so Starlette can't complain
templates_dir = BASE_DIR / "templates"
static_dir = BASE_DIR / "static"
templates_dir.mkdir(parents=True, exist_ok=True)
static_dir.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory=str(templates_dir))
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/notebook")
def notebook(limit: int = 20):
    db = SessionLocal()
    try:
        rows = db.query(Experiment).order_by(desc(Experiment.id)).limit(limit).all()
        items = []
        for r in rows:
            items.append({
                "id": r.id,
                "created_at": r.created_at,
                "reagents": json.loads(r.reagents),
                "result": json.loads(r.result),
            })
        return {"items": items}
    finally:
        db.close()


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


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/chemicals")
def chemicals():
    return {"items": load_reagents()}