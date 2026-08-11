from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, fhir, report, system, triage
from app.core.middleware import request_middleware
from app.core.version import APP_VERSION, version_info

app = FastAPI(
    title="ClinicalTriage AI API",
    version=APP_VERSION,
    description="Clinical decision-support API. Not a substitute for professional medical judgment or emergency care.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://triage.mustafalsalem.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)
app.middleware("http")(request_middleware)

app.include_router(auth.router)
app.include_router(system.router)
app.include_router(triage.router)
app.include_router(fhir.router)
app.include_router(report.router)

@app.get("/")
def root():
    return {"message": "Clinical Triage API", "version": APP_VERSION, "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "healthy", "version": APP_VERSION}

@app.get("/version")
def version():
    return version_info()
