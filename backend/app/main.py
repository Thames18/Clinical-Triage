from fastapi import FastAPI

app = FastAPI(
    title="Clinical Triage AI API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Clinical Triage API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }