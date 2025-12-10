# main.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
import logging

# --- Güvenlik Ayarları ---
security = HTTPBearer()
GIZLI_TOKEN = "furkan123"  # Bu bizim API şifremiz

def token_dogrula(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Kullanıcının gönderdiği token'ı kontrol eder.
    """
    token = credentials.credentials
    if token != GIZLI_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Geçersiz Token! Giriş izniniz yok."
        )
    return token

# --- Pydantic Modelleri ---
class PlanCreate(BaseModel):
    mesaj: str
    saat: str

class Plan(BaseModel):
    id: int
    mesaj: str
    saat: str

# --- Sanal Veritabanı ---
db_planlar: List[Plan] = [
    Plan(id=1, mesaj="Varsayılan Plan", saat="09:00")
]
mevcut_id = 1

# --- FastAPI Uygulaması ---
app = FastAPI(title="Günlük Plan API (Güvenlikli)")

# CORS Ayarları (Frontend'in Backend ile konuşabilmesi için şart)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Her yerden gelen isteği kabul et (Test için)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpointler ---

# 1. HERKESİN Erişebileceği Açık Endpoint
@app.get("/")
def ana_sayfa():
    return {"mesaj": "Hoşgeldiniz! Planları görmek için yetkili olmalısınız."}

# 2. SADECE ŞİFRESİ OLANIN Erişebileceği Endpoint (Kilitli)
@app.get("/planlar/", response_model=List[Plan])
def planlari_listele(token: str = Depends(token_dogrula)):
    """
    Bu endpoint kilitlidir. Sadece doğru Bearer Token gönderenler görebilir.
    """
    return db_planlar

@app.post("/planlar/", response_model=Plan)
def plan_olustur(plan_data: PlanCreate, token: str = Depends(token_dogrula)):
    """
    Plan eklemek için de şifre gerekir.
    """
    global mevcut_id
    mevcut_id += 1
    yeni_plan = Plan(id=mevcut_id, mesaj=plan_data.mesaj, saat=plan_data.saat)
    db_planlar.append(yeni_plan)
    return yeni_plan