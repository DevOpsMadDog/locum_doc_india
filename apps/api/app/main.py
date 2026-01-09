from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import admin, auth, clinic, doctor, otp, payments, realtime

app = FastAPI(title="LocumMap Chennai API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(clinic.router)
app.include_router(doctor.router)
app.include_router(otp.router)
app.include_router(payments.router)
app.include_router(admin.router)
app.include_router(realtime.router)


@app.get("/")
def root() -> dict:
    return {"status": "ok"}
