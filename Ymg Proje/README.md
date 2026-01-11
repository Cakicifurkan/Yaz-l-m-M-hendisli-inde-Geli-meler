# Yazılım Mimarisi ve Tasarımı - Veritabanı ve Docker Entegrasyonu

Bu proje, bir Python (FastAPI/Uvicorn) backend uygulamasının PostgreSQL veritabanı ile Docker üzerinde birlikte çalıştırılmasını göstermektedir.

## Ödev Kapsamında Yapılanlar
- **Veritabanı Bağlantısı:** SQLAlchemy kullanılarak PostgreSQL veritabanı bağlantısı sağlandı.
- **Konteynerleştirme:** Uygulama ve veritabanı servisleri `docker-compose.yml` dosyası ile yapılandırıldı.
- **Otomatik Tablo Oluşturma:** Uygulama ayağa kalktığında veritabanı modelleri otomatik olarak PostgreSQL üzerinde oluşturulmaktadır.

## Projeyi Çalıştırma

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

1. Projeyi klonlayın:
   ```bash
   git clone <repository-url>

2.Proje dizinine gidin:
   cd <proje-klasor-adi>

3.Docker servislerini ayağa kaldırın:
   docker-compose up --build



API Kullanımı
Uygulama ayağa kalktıktan sonra aşağıdaki adreslerden erişim sağlayabilirsiniz:

Backend API: http://localhost:8000

Swagger UI (Dokümantasyon): http://localhost:8000/docs

Dosya Yapısı
backend/: API kodlarını ve veritabanı modellerini içerir.

db/: Veritabanı yapılandırmalarını içerir (Eğer varsa).

docker-compose.yml: Servislerin orkestrasyonunu sağlar.


---

### 3. Son Kontrol: `requirements.txt`
Eğer `backend-api` klasörünün içinde `requirements.txt` dosyan varsa, içinde şunların olduğundan emin ol (Kopyalayıp içine ekleyebilirsin):

```text
fastapi
uvicorn
sqlalchemy
psycopg2-binary