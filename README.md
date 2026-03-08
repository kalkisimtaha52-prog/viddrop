![Demo](assets/EkranKayd2026-03-08122944-ezgif.com-video-to-gif-converter.gif)# 

🎬 VidDrop — YouTube Video İndirici

Kendi bilgisayarında çalışan, yüksek kaliteli YouTube video indirme uygulaması.

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-3.1-green) ![yt--dlp](https://img.shields.io/badge/yt--dlp-latest-red)

---

## ✨ Özellikler

- 🎬 4K, 1080p, 720p, 480p, 360p kalite seçimi
- 🎵 MP3 ses indirme (320kbps)
- 📊 Gerçek zamanlı indirme progress bar
- 🖼️ Video önizleme (thumbnail, süre, izlenme sayısı)
- 💾 İndirilenler otomatik `downloads/` klasörüne kaydedilir
- 🪟 Windows Media Player uyumlu MP4 çıktısı

---

## 📦 Kurulum

### 1. Gereksinimler

- [Python 3.8+](https://www.python.org/downloads/) — kurulumda **"Add Python to PATH"** seçeneğini işaretle ✅
- [ffmpeg](https://www.gyan.dev/ffmpeg/builds/) — `ffmpeg-release-essentials.zip` indir, içinden `ffmpeg.exe`'yi proje klasörüne koy

### 2. Projeyi İndir

```bash
git clone https://github.com/kursat-dev/viddrop
cd viddrop
```

Ya da ZIP olarak indir → klasöre çıkart.

### 3. Kütüphaneleri Kur

```bash
pip install -r requirements.txt
```

### 4. ffmpeg'i Kur

👉 https://www.gyan.dev/ffmpeg/builds/ adresinden `ffmpeg-release-essentials.zip` indir

Zip içindeki `bin/ffmpeg.exe` dosyasını proje klasörüne koy:

```
viddrop/
├── app.py
├── ffmpeg.exe   ← buraya
├── index.html
└── ...
```

---

## 🚀 Kullanım

### Yöntem 1 — Docker (Önerilen) 🐳
Eğer bilgisayarında Docker varsa, Python veya ffmpeg kurmakla uğraşmadan tek satırla çalıştırabilirsin:
```bash
docker compose up -d
```
Tarayıcıda aç: **http://localhost:5000** (İndirilen videolar proje klasöründeki `downloads/` içine otomatik gelir)

### Yöntem 2 — Çift Tıkla (Windows İçin Kolay)
`BAŞLAT.bat` dosyasına çift tıkla. Site otomatik açılır.

### Yöntem 3 — Terminal (Eski Usul - MacOS/Linux Uyumlu)
Terminali açıp proje klasörüne gidin ve sırasıyla şu komutları çalıştırın:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Tarayıcıda aç: **http://127.0.0.1:5000**

---

## 📁 Klasör Yapısı

```
viddrop/
├── app.py              # Uygulama giriş noktası
├── src/                # Backend servisleri ve rotaları
│   ├── app.py          # Flask uygulaması kurulumu
│   ├── routes/         # API Endpoint'leri
│   └── services/       # İndirme ve temizleme lojiği
├── public/             # Frontend statik dosyaları (HTML, CSS, JS)
├── requirements.txt    # Kütüphaneler
├── Dockerfile          # Docker kurulum dosyası
├── docker-compose.yml  # Docker compose dosyası
├── BAŞLAT.bat          # Tek tıkla başlat (Windows)
├── ffmpeg.exe          # Sen koyacaksın (Windows için)
└── downloads/          # İndirilen videolar buraya gelir
```

---

## ❓ Sık Sorulan Sorular

**Video inmiyor?**
```bash
pip install -U yt-dlp
```

**Ses yok mu?**
`ffmpeg.exe` dosyasının proje klasöründe olduğundan emin ol.

**pip tanınmıyor mu?**
Python'u "Add to PATH" seçeneğiyle tekrar kur.

---

## ⚠️ Yasal Uyarı

Bu proje yalnızca **kişisel kullanım** içindir. Telif hakkıyla korunan içerikleri indirmek ilgili platformların kullanım şartlarına aykırı olabilir. Sorumluluk kullanıcıya aittir.

---

## 🛠️ Kullanılan Teknolojiler

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Flask](https://flask.palletsprojects.com/)
- [ffmpeg](https://ffmpeg.org/)
