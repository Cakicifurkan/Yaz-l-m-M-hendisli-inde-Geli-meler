from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("PlanMaster AI")

@mcp.tool()
def gorevi_parcala(gorev: str) -> str:
    """Karmaşık bir görevi 3 alt adıma böler."""
    gorev = gorev.lower()
    if "docker" in gorev:
        return "1. Dockerfile hazırla\n2. Image build et\n3. Container çalıştır"
    elif "sınav" in gorev or "ders" in gorev:
        return "1. Konu özetlerini oku\n2. Çıkmış soruları çöz\n3. Tekrar yap"
    elif "yazılım" in gorev or "kod" in gorev:
        return "1. Algoritmayı kur\n2. Kodlamaya başla\n3. Test et ve debug yap"
    else:
        return f"1. {gorev} için hazırlık yap\n2. Ana işi tamamla\n3. Son kontrolleri yap"

@mcp.tool()
def gunu_analiz_et(gorev_sayisi: int) -> str:
    """Günün yoğunluğuna göre tavsiye verir."""
    if gorev_sayisi == 0:
        return "Bugün çok boşsun, kendine bir hedef belirle! 🚀"
    elif gorev_sayisi <= 3:
        return "Rahat bir gün. Kaliteye odaklanabilirsin. ☕"
    elif gorev_sayisi <= 6:
        return "Dolu bir gün seni bekliyor. Enerjini iyi yönet. 💪"
    else:
        return "Çok yoğun! Acil olmayanları ertelemeyi düşün. 🔥"

if __name__ == "__main__":
    mcp.run()