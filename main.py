from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# --- Veritabanı Ayarları ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://furkan_user:furkan_password@db:5432/plan_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Veritabanı Modeli (Tablo Yapısı)
class PlanDB(Base):
    __tablename__ = "planlar"
    id = Column(Integer, primary_key=True, index=True)
    mesaj = Column(String)
    saat = Column(String)

# Tabloları otomatik oluştur (Hoca için artı puan)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Günlük Plan API (DB Bağlantılı)")

# Veritabanı oturumu açma/kapama fonksiyonu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpointler ---

@app.get("/planlar/")
def planlari_listele(db: Session = Depends(get_db)):
    return db.query(PlanDB).all()

@app.post("/planlar/")
def plan_olustur(mesaj: str, saat: str, db: Session = Depends(get_db)):
    yeni_plan = PlanDB(mesaj=mesaj, saat=saat)
    db.add(yeni_plan)
    db.commit()
    db.refresh(yeni_plan)
    return yeni_plan
