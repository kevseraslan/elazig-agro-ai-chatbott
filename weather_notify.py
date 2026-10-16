import os
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Istanbul")
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
ILCE = os.environ.get("AGRO_ILCE", "Baskil")

KOORDINATLAR = {
    "Merkez": (38.6748, 39.2225),
    "Baskil": (38.5680, 38.8240),
    "Keban": (38.7940, 38.7440),
    "Sivrice": (38.4480, 39.3080),
    "Palu": (38.6910, 39.9280),
    "Kovancılar": (38.7180, 39.8640),
    "Karakoçan": (38.9560, 40.0390),
    "Maden": (38.3890, 39.6710),
    "Ağın": (38.9370, 38.7110),
    "Alacakaya": (38.4630, 39.8620),
    "Arıcak": (38.5650, 40.1360)
}

def telegram_gonder(metin):
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": metin},
        timeout=20
    )
    r.raise_for_status()
    veri = r.json()
    if not veri.get("ok"):
        raise RuntimeError(veri.get("description", "Telegram hatası"))

def gorev_kontrol():
    dosya = Path("gorevler.json")
    if not dosya.exists():
        return

    bugun = datetime.now(TZ).date().isoformat()
    gorevler = json.loads(dosya.read_text(encoding="utf-8"))

    for gorev in gorevler:
        if gorev.get("tamamlandi"):
            continue
        if gorev.get("tarih") == bugun:
            bir_kez_gonder(
                f"gorev:{bugun}:{gorev.get('id', gorev['baslik'])}",
                "🔔 ELAZIĞ AGRO AI — GÖREV\n\n"
                f"📅 {bugun}\n"
                f"🌱 {gorev['baslik']}"
            )

def hava_kontrol():
    lat, lon = KOORDINATLAR.get(ILCE, KOORDINATLAR["Merkez"])

    r = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": (
                "temperature_2m,precipitation,snowfall,"
                "wind_gusts_10m,weather_code"
            ),
            "forecast_days": 3,
            "timezone": "Europe/Istanbul"
        },
        timeout=25
    )
    r.raise_for_status()
    saatlik = r.json()["hourly"]

    simdi = datetime.now(TZ)
    bitis = simdi + timedelta(hours=48)

    riskler = {}

    for i, zaman in enumerate(saatlik["time"]):
        an = datetime.fromisoformat(zaman).replace(tzinfo=TZ)
        if not simdi <= an <= bitis:
            continue

        sicaklik = saatlik["temperature_2m"][i]
        yagis = saatlik["precipitation"][i]
        kar = saatlik["snowfall"][i]
        hamle = saatlik["wind_gusts_10m"][i]
        kod = saatlik["weather_code"][i]

        gun = zaman[:10]

        if sicaklik is not None and sicaklik <= 2:
            riskler[("DON", gun)] = f"{sicaklik}°C"

        if yagis is not None and yagis >= 10:
            riskler[("KUVVETLİ YAĞMUR", gun)] = f"{yagis} mm/saat"

        if (kar or 0) > 0 or kod in (71, 73, 75, 77, 85, 86):
            riskler[("KAR", gun)] = f"{kar or 0} cm/saat"

        if kod in (96, 99):
            riskler[("DOLU İHTİMALİ", gun)] = f"Kod {kod}"

        if hamle is not None and hamle >= 65:
            riskler[("KUVVETLİ RÜZGÂR", gun)] = f"{hamle} km/sa"

        if kod in (95, 96, 99):
            riskler[("FIRTINA", gun)] = f"Kod {kod}"

    for (tur, gun), deger in sorted(riskler.items()):
        bir_kez_gonder(
            f"hava:{ILCE}:{tur}:{gun}",
            "⚠️ ELAZIĞ AGRO AI — HAVA UYARISI\n\n"
            f"📍 {ILCE}\n"
            f"📅 {gun}\n"
            f"🌦️ {tur}: {deger}\n\n"
            "İlçe merkezi model tahminidir; "
            "resmî meteorolojik uyarı değildir."
        )


DURUM_DOSYASI = Path("bildirim_durumu.json")

def durum_oku():
    if DURUM_DOSYASI.exists():
        return json.loads(
            DURUM_DOSYASI.read_text(encoding="utf-8")
        )
    return {}

def durum_kaydet(durum):
    DURUM_DOSYASI.write_text(
        json.dumps(durum, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def bir_kez_gonder(anahtar, mesaj):
    durum = durum_oku()

    if anahtar in durum:
        print("Önceden bildirildi:", anahtar)
        return False

    telegram_gonder(mesaj)

    durum[anahtar] = datetime.now(TZ).isoformat()
    durum_kaydet(durum)

    print("Yeni bildirim:", anahtar)
    return True

if __name__ == "__main__":
    gorev_kontrol()
    hava_kontrol()
