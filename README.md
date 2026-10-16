# 🌱 Elazığ Akıllı Tarım Asistanı — Agro AI V7

Elazığ'daki çiftçilerin tarımsal bilgiye erişimini kolaylaştırmak amacıyla geliştirilmiş, yapay zekâ destekli bir tarımsal karar destek sistemi prototipidir.

## 🚀 Özellikler

- **Akıllı Tarım Asistanı:** Claude yapay zekâ modeliyle Türkçe soru-cevap
- **PDF Destekli RAG:** FAISS ve BM25 kullanarak tarımsal belgelerden bilgi arama
- **Bitki Fotoğraf Analizi:** Görseller üzerinden ön değerlendirme
- **Otomatik Tarım Planı:** Kaynaklara dayalı görev önerileri ve kullanıcı onayı
- **Sesli Asistan:** Türkçe sesli soru ve yanıt
- **Hava Durumu:** Open-Meteo hava tahminleri
- **Tarım Takvimi:** Görev ekleme ve tamamlama
- **Bahçe Günlüğü:** Tarımsal faaliyetlerin kaydı
- **Çiftçi Profili:** İlçe, ürün ve bahçe bilgilerinin yönetimi
- **Telegram Bildirimleri:** GitHub Actions üzerinden zamanlanmış kontrol ve bildirimler
- **Gradio V7 Arayüzü:** Özellikleri bir araya getiren kullanıcı paneli

## 🧠 Kullanılan Teknolojiler

Python, Google Colab, Anthropic Claude, Gradio, FAISS, BM25, Sentence Transformers, Open-Meteo, Telegram Bot API ve GitHub Actions.

## 📂 Proje Dosyaları

- `Agro_AI_V7.ipynb` — Yapay zekâ asistanının Colab notebook'u
- `requirements.txt` — Python bağımlılıkları
- `weather_notify.py` — Hava durumu bildirim kodu
- `gorevler.json` — Bildirim otomasyonunun görev verileri
- `.github/workflows/` — Zamanlanmış GitHub Actions iş akışı

## ▶️ Çalıştırma

1. `Agro_AI_V7.ipynb` dosyasını Google Colab'da açın.
2. Gerekli kütüphaneleri yükleyin.
3. Tarımsal PDF belgelerini uygun klasöre ekleyin.
4. API anahtarlarını güvenli ortam değişkenleri veya Colab Secrets üzerinden tanımlayın.
5. Notebook hücrelerini sırayla çalıştırın.

**Not:** Notebook'un temiz bir Colab oturumunda baştan sona çalıştırılması henüz doğrulanmamıştır. Ek dosya ve yapılandırma gerektirebilir.

## 🎯 Projenin Amacı

Elazığ'da özellikle kayısı, ceviz ve bağ yetiştiriciliği alanlarında çiftçilere anlaşılır, kaynak destekli ve erişilebilir tarımsal bilgi sunmak.

## ⚠️ Sınırlamalar

Bu sistem bir prototiptir. Yapay zekâ yanıtları ve PDF sayfa atıfları ayrıca doğrulanmalıdır. Görsel analiz kesin hastalık teşhisi değildir. Tarımsal ilaçlama ve gübreleme kararlarında yetkili uzman görüşü alınmalıdır.

## 📌 Geliştirme Hedefleri

Kayısı yetiştiriciliğine yönelik bilgi tabanının genişletilmesi, kaynak doğrulama sisteminin iyileştirilmesi ve bahçe verileriyle daha kişiselleştirilmiş öneriler üretilmesi.
