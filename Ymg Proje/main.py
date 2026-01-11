from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
import os
import secrets
import string
import random
import requests 
from datetime import datetime
from google import genai  # ✅ YENİ KÜTÜPHANE

# --- VERİTABANI AYARLARI ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://furkan_user:furkan_password@db:5432/plan_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODEL ---
class PlanDB(Base):
    __tablename__ = "planlar"
    id = Column(Integer, primary_key=True, index=True)
    mesaj = Column(String, index=True)
    saat = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- GÜVENLİK (BEARER TOKEN) ---
security = HTTPBearer()

def token_kontrol(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != "furkan123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz Token! Erişim Reddedildi.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

# --- MERMAID DIYAGRAMI ---
@app.get("/sema/mermaid")
def sema_getir():
    mermaid_code = """
    sequenceDiagram
        participant K as Kullanıcı (Frontend)
        participant A as API (FastAPI)
        participant D as Veritabanı (PostgreSQL)
        
        K->>A: GET /planlar/ (Token Kontrolü)
        alt Token Geçerli
            A->>D: SELECT * FROM planlar
            D-->>A: [Plan1, Plan2...]
            A-->>K: JSON Yanıtı
        else Token Geçersiz
            A-->>K: 401 Unauthorized
        end
    """
    return {"mermaid_code": mermaid_code}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- KORUMALI API ENDPOINTLERİ (Token İster) ---

@app.get("/planlar/")
def planlari_getir(db: Session = Depends(get_db), token: str = Depends(token_kontrol)):
    return db.query(PlanDB).all()

@app.post("/planlar/")
def plan_ekle(mesaj: str, saat: str, db: Session = Depends(get_db), token: str = Depends(token_kontrol)):
    yeni_plan = PlanDB(mesaj=mesaj, saat=saat)
    db.add(yeni_plan)
    db.commit()
    db.refresh(yeni_plan)
    return yeni_plan

@app.delete("/planlar/{plan_id}")
def plan_sil(plan_id: int, db: Session = Depends(get_db), token: str = Depends(token_kontrol)):
    plan = db.query(PlanDB).filter(PlanDB.id == plan_id).first()
    if plan:
        db.delete(plan)
        db.commit()
    return {"durum": "Silindi"}

@app.put("/planlar/{plan_id}")
def plan_guncelle(plan_id: int, mesaj: str, saat: str, db: Session = Depends(get_db), token: str = Depends(token_kontrol)):
    plan = db.query(PlanDB).filter(PlanDB.id == plan_id).first()
    if plan:
        plan.mesaj = mesaj
        plan.saat = saat
        db.commit()
    return plan

# --- GENEL API ENDPOINTLERİ (Token İstemez) ---

# 👇👇👇 BURAYA KENDİ KEY'İNİ YAPIŞTIRMAYI UNUTMA! 👇👇👇
GEMINI_API_KEY = "AIzaSyBajOptcL5yfETYUI-TQ0m2DFztxDjAdpA"

# İstemciyi (Client) Oluştur
client = genai.Client(api_key=GEMINI_API_KEY)

@app.get("/ai/parcala")
def gorev_parcala(gorev: str):
    try:
        prompt = f"'{gorev}' adlı görevi gerçekleştirmek için bana 3 tane çok kısa, net ve uygulanabilir alt adım maddesi çıkar. Sadece maddeleri yaz, emoji kullan."
        
        # ✅ YENİ KÜTÜPHANE KULLANIMI
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        
        return {"sonuc": response.text}
        
    except Exception as e:
        print(f"AI Hatası: {e}")
        return {"sonuc": f"1. {gorev} için araştırma yap 🔍\n2. Planla 📝\n3. Uygula 🚀"}

@app.get("/ai/analiz")
def gunu_analiz_et(db: Session = Depends(get_db)):
    sayi = db.query(PlanDB).count()
    if sayi == 0: msg = "Bomboş bir gün! Hedef belirle. 🚀"
    elif sayi <= 3: msg = "Sakin bir gün. Tadını çıkar. ☕"
    elif sayi <= 6: msg = "Verimli bir gün. Devam et! 💪"
    else: msg = "Çok yoğunsun! Bazılarını erteleyebilirsin. 🔥"
    return {"analiz": msg, "sayi": sayi}

@app.get("/ai/sirala")
def akilli_sirala(db: Session = Depends(get_db)):
    planlar = db.query(PlanDB).all()
    onemli = ["acil", "sınav", "önemli", "deadline", "kritik"]
    sirali = sorted(planlar, key=lambda x: any(k in x.mesaj.lower() for k in onemli), reverse=True)
    return sirali

@app.get("/araclar/sifre-uret")
def sifre_uret(uzunluk: int = 12):
    havuz = string.ascii_letters + string.digits + "!@#$%&"
    sifre = ''.join(secrets.choice(havuz) for _ in range(uzunluk))
    return {"sonuc": sifre}

@app.get("/araclar/sure-hesapla")
def sure_hesapla(baslangic: str, bitis: str):
    try:
        t1 = datetime.strptime(baslangic, "%H:%M")
        t2 = datetime.strptime(bitis, "%H:%M")
        if t2 < t1: return {"hata": "Bitiş saati hatalı."}
        fark = t2 - t1
        return {"sonuc": f"{fark.seconds // 3600} saat {(fark.seconds % 3600) // 60} dakika"}
    except: return {"hata": "Format hatası."}

@app.get("/aktivite-oner")
def aktivite_oner():
    try:
        res = requests.get("https://bored-api.appbrewery.com/random", timeout=2)
        if res.status_code == 200:
            data = res.json()
            return {"oneri": data['activity'], "tur": data['type']}
    except: pass
    
    yedek = [
        {"oneri": "GitHub profilini güncelle", "tur": "Kariyer"},
        {"oneri": "5 dakika gözlerini dinlendir", "tur": "Sağlık"},
        {"oneri": "Linkedin bağlantılarını kontrol et", "tur": "Network"}
    ]
    return random.choice(yedek)