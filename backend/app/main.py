from fastapi import FastAPI

app = FastAPI(title="Virtual Lab")

@app.get("/health")
def health():
    return {"status": "ok"}