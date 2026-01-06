from mcp.server.fastmcp import FastMCP
from datetime import datetime
import secrets
import string

# Servisin adı artık daha havalı
mcp = FastMCP("PlanMaster AI Tools")

# --- TOOL 1: Süre Hesaplayıcı (Planlama için) ---
@mcp.tool()
def sure_hesapla(baslangic_saati: str, bitis_saati: str) -> str:
    """
    İki saat arasındaki süreyi hesaplar.
    Örnek kullanım: baslangic_saati="09:00", bitis_saati="14:30"
    """
    fmt = "%H:%M"
    try:
        t1 = datetime.strptime(baslangic_saati, fmt)
        t2 = datetime.strptime(bitis_saati, fmt)
        
        # Eğer bitiş saati başlangıçtan küçükse (gece yarısı geçişi)
        if t2 < t1:
             return "Hata: Bitiş saati başlangıçtan önce olamaz."
             
        fark = t2 - t1
        saat = fark.seconds // 3600
        dakika = (fark.seconds % 3600) // 60
        
        return f"Bu iki saat arasında toplam {saat} saat {dakika} dakika zaman var."
    except ValueError:
        return "Lütfen saati HH:MM formatında gir (Örn: 14:30)"

# --- TOOL 2: Güvenli Şifre Oluşturucu (Utility) ---
@mcp.tool()
def guclu_sifre_uret(uzunluk: int = 12) -> str:
    """
    Belirtilen uzunlukta kırılması zor, rastgele bir şifre oluşturur.
    Varsayılan uzunluk: 12 karakter.
    """
    # Harfler, sayılar ve özel karakterlerden oluşan havuz
    karakterler = string.ascii_letters + string.digits + "!@#$%&*"
    
    # Rastgele seçim yap
    sifre = ''.join(secrets.choice(karakterler) for _ in range(uzunluk))
    return f"Oluşturulan Güvenli Şifre: {sifre}"

if __name__ == "__main__":
    mcp.run()