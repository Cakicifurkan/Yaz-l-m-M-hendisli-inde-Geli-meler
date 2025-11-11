# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging

# --- Pydantic Modelleri (API'nin ne tür veri alıp vereceğini tanımlar) ---

# UI'dan (Arayüzden) yeni plan oluşturmak için gelecek olan veri
class PlanCreate(BaseModel):
    mesaj: str
    saat: str  # Örn: "20:00"

# Kullanıcıya cevap olarak döneceğimiz veri (ID'si ile birlikte)
class Plan(BaseModel):
    id: int
    mesaj: str
    saat: str

# --- Sanal Veritabanı ---
# Gerçek bir veritabanı kurmakla uğraşmıyoruz.
# Planları bu listede tutacağız.
db_planlar: List[Plan] = []
mevcut_id = 0

# --- FastAPI Uygulaması ---
app = FastAPI(
    title="Günlük Plan Takip Uygulaması API",
    description="Sequence diyagramına dayalı basit planlama API'si. Bu dokümantasyon (Swagger) FastAPI tarafından otomatik olarak oluşturulmuştur.",
    version="1.0.0"
)

# --- API Endpointleri (Uç Noktalar) ---

@app.post("/planlar/", response_model=Plan, status_code=201)
def plan_olustur(plan_data: PlanCreate):
    """
    Sequence Diyagramı: UI ->> Backend
    
    Yeni bir plan ve bildirim kaydı oluşturur.
    - **mesaj**: Bildirim metni (örn: "Ders çalış")
    - **saat**: Bildirim saati (örn: "21:30")
    """
    global mevcut_id
    
    # 1. Adım: Planı kaydet (Diyagramdaki 'Backend ->> DB')
    mevcut_id += 1
    yeni_plan = Plan(id=mevcut_id, mesaj=plan_data.mesaj, saat=plan_data.saat)
    db_planlar.append(yeni_plan)
    
    print(f"VERİTABANI (Sanal): Plan kaydedildi -> {yeni_plan.dict()}")

    # 2. Adım: Bildirimi planla (Diyagramdaki 'Backend ->> Notification')
    # Gerçek bir bildirim servisi yok, bu yüzden konsola yazdırıyoruz.
    logging.info(f"BİLDİRİM SERVİSİ (Sanal): '{yeni_plan.mesaj}' için {yeni_plan.saat} saatine bildirim planlandı.")
    
    # 3. Adım: UI'a cevap dön (Diyagramdaki 'Backend -->> UI')
    return yeni_plan

@app.get("/planlar/", response_model=List[Plan])
def tum_planlari_getir():
    """
    Kaydedilen tüm planları listeler. (Ödevde zorunlu değil ama test için faydalı)
    """
    return db_planlar

@app.get("/planlar/{plan_id}", response_model=Plan)
def plani_getir(plan_id: int):
    """
    ID'ye göre tek bir planı getirir.
    """
    for plan in db_planlar:
        if plan.id == plan_id:
            return plan
    # Bulamazsa 404 hatası döner
    raise HTTPException(status_code=404, detail="Plan bulunamadı")