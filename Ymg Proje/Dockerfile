
FROM python:3.12-slim

# Çalışma klasörünü ayarla
WORKDIR /app

# Gereksinim dosyasını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kalan tüm dosyaları (main.py vb.) kopyala
COPY . .

# Uygulamayı çalıştır (Önemli: host 0.0.0.0 olmalı ki dışarıdan erişilebilsin)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]