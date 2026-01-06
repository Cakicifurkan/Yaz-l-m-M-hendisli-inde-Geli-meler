from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import requests
import secrets
import string
from datetime import datetime

# --- Veritabanı Ayarları ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://furkan_user:furkan_password@db:5432/plan_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Veritabanı Modeli
class PlanDB(Base):
    __tablename__ = "planlar"
    id = Column(Integer, primary_key=True, index=True)
    mesaj = Column(String)
    saat = Column(String)

# Tabloları oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Günlük Plan API (DB Bağlantılı)")

# --- CORS AYARLARI (ÖNEMLİ: Frontend erişimi için) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm kaynaklara izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Veritabanı Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Basit Güvenlik Kontrolü ---
def token_kontrol(authorization: str = Header(None)):
    # Frontend "Bearer furkan123" gönderiyor, biz de bunu kontrol ediyoruz
    if authorization != "Bearer furkan123":
        raise HTTPException(status_code=403, detail="Geçersiz Token")

# --- Endpointler ---

@app.get("/planlar/")
def planlari_listele(db: Session = Depends(get_db), auth: str = Depends(token_kontrol)):
    return db.query(PlanDB).all()

@app.post("/planlar/")
def plan_olustur(mesaj: str, saat: str, db: Session = Depends(get_db), auth: str = Depends(token_kontrol)):
    yeni_plan = PlanDB(mesaj=mesaj, saat=saat)
    db.add(yeni_plan)
    db.commit()
    db.refresh(yeni_plan)
    return yeni_plan



# --- AKTİVİTE ÖNERİSİ (Hocanın İstediği Dış API Özelliği) ---
@app.get("/aktivite-oner")
def aktivite_getir():
    try:
        # BoredAPI: Rastgele etkinlik öneren ücretsiz bir servis
        # Timeout=5 saniye bekler, cevap gelmezse hata verir
        url = "https://bored-api.appbrewery.com/random"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            # Gelen veriyi (activity ve type) döndürüyoruz
            return {"oneri": data['activity'], "tur": data['type']}
        else:
            # API çalışmazsa yedek bir plan döndür
            return {"oneri": "Docker belgelerini oku", "tur": "education"}
            
    except Exception as e:
        # İnternet yoksa burası çalışır
        return {"oneri": "Kodlarını tekrar gözden geçir", "tur": "work"}
    


    # --- SİLME İŞLEMİ (DELETE) ---
@app.delete("/planlar/{plan_id}")
def plan_sil(plan_id: int, db: Session = Depends(get_db), auth: str = Depends(token_kontrol)):
    plan = db.query(PlanDB).filter(PlanDB.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan bulunamadı")
    
    db.delete(plan)
    db.commit()
    return {"durum": "Silindi"}

# --- GÜNCELLEME İŞLEMİ (PUT) ---
@app.put("/planlar/{plan_id}")
def plan_guncelle(plan_id: int, mesaj: str, saat: str, db: Session = Depends(get_db), auth: str = Depends(token_kontrol)):
    plan = db.query(PlanDB).filter(PlanDB.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan bulunamadı")
    
    plan.mesaj = mesaj
    plan.saat = saat
    db.commit()
    db.refresh(plan)
    return plan



# --- ARAÇLAR (Tools) ENDPOINTLERİ ---

@app.get("/araclar/sifre-uret")
def sifre_uret(uzunluk: int = 12):
    # Harfler ve rakamlardan oluşan havuz
    havuz = string.ascii_letters + string.digits + "!@#$%&"
    sifre = ''.join(secrets.choice(havuz) for _ in range(uzunluk))
    return {"sonuc": sifre}

@app.get("/araclar/sure-hesapla")
def sure_hesapla(baslangic: str, bitis: str):
    try:
        fmt = "%H:%M"
        t1 = datetime.strptime(baslangic, fmt)
        t2 = datetime.strptime(bitis, fmt)
        
        if t2 < t1:
            return {"hata": "Bitiş saati başlangıçtan küçük olamaz."}
            
        fark = t2 - t1
        saat = fark.seconds // 3600
        dakika = (fark.seconds % 3600) // 60
        
        return {"sonuc": f"{saat} saat {dakika} dakika"}
    except:
        return {"hata": "Saat formatı hatalı."}