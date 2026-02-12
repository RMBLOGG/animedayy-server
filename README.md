# 📱 AnimeDayy Update Manager API

API Flask untuk mengelola update aplikasi Android AnimeDayy. Bisa di-deploy ke Vercel dengan mudah.

## 🚀 Cara Deploy ke Vercel

### Persiapan

1. **Install Git** (jika belum)
   - Download dari https://git-scm.com/

2. **Buat akun Vercel** (gratis)
   - Daftar di https://vercel.com/signup
   - Login menggunakan GitHub (recommended)

3. **Install Vercel CLI** (opsional, tapi recommended)
   ```bash
   npm install -g vercel
   ```

### Langkah Deploy

#### Opsi 1: Deploy via GitHub (Recommended)

1. **Buat Repository GitHub Baru**
   - Buka https://github.com/new
   - Beri nama: `animedayy-update-api`
   - Buat repository (public atau private)

2. **Upload File ke GitHub**
   ```bash
   # Di folder project ini, jalankan:
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/USERNAME/animedayy-update-api.git
   git push -u origin main
   ```

3. **Deploy di Vercel**
   - Buka https://vercel.com/new
   - Pilih "Import Git Repository"
   - Pilih repository `animedayy-update-api`
   - Klik "Deploy"
   - Tunggu selesai (1-2 menit)

4. **Dapatkan URL**
   - Setelah deploy selesai, Anda akan dapat URL seperti:
   - `https://animedayy-update-api.vercel.app`

#### Opsi 2: Deploy via Vercel CLI

```bash
# Di folder project ini, jalankan:
vercel

# Ikuti instruksi:
# - Set up and deploy? Yes
# - Which scope? (pilih akun Anda)
# - Link to existing project? No
# - What's your project's name? animedayy-update-api
# - In which directory is your code located? ./
# - Want to override settings? No

# Deploy production:
vercel --prod
```

#### Opsi 3: Deploy Manual (Drag & Drop)

1. Buka https://vercel.com/new
2. Pilih tab "Deploy from template"
3. Klik "Browse" atau drag & drop folder project
4. Klik "Deploy"

## 🔧 Update URL di Android App

Setelah deploy, update `AppUpdateChecker.java`:

```java
// Ubah dari:
private static final String UPDATE_API_URL = "http://127.0.0.1:5000/api/check-update";

// Menjadi:
private static final String UPDATE_API_URL = "https://your-app-name.vercel.app/api/check-update";
```

Ganti `your-app-name` dengan nama project Vercel Anda.

## 📝 Cara Menggunakan

### Admin Panel
- URL: `https://your-app-name.vercel.app`
- Bisa diakses langsung di browser
- Input informasi update di form
- Klik "Simpan Update Info"

### API Endpoints

**1. Check Update**
```
GET https://your-app-name.vercel.app/api/check-update?current_version_code=1
```

Response:
```json
{
  "has_update": true,
  "current_version": 1,
  "latest_version": 2,
  "latest_version_name": "1.1.0",
  "update_required": false,
  "update_title": "Update Tersedia!",
  "update_message": "Versi baru dengan fitur menarik",
  "download_url": "https://example.com/app.apk",
  "whats_new": [
    "Fitur bookmark",
    "Perbaikan bug"
  ]
}
```

**2. Get Update Info**
```
GET https://your-app-name.vercel.app/api/update-info
```

## ⚠️ Catatan Penting

### Limitasi Vercel Free Tier
- **Tidak ada persistent storage**: Data disimpan di `/tmp` dan akan hilang setelah beberapa waktu
- **Solusi**: Setiap kali ada update baru, input kembali di admin panel
- **Alternatif**: Gunakan database eksternal (PostgreSQL, MongoDB, dll) untuk production

### Untuk Production (Recommended)
Jika aplikasi Anda akan digunakan secara luas, pertimbangkan:

1. **Gunakan Database Cloud** (gratis):
   - Supabase PostgreSQL
   - MongoDB Atlas
   - PlanetScale MySQL

2. **Atau deploy ke hosting lain**:
   - Railway.app (recommended, ada free tier)
   - Heroku (berbayar)
   - DigitalOcean App Platform ($5/bulan)

## 🔒 Security

Untuk production, tambahkan:
- Authentication untuk admin panel
- Rate limiting
- CORS configuration
- Environment variables untuk sensitive data

## 📞 Support

Jika ada masalah saat deploy:
1. Cek Vercel deployment logs
2. Pastikan semua file sudah ter-upload
3. Cek `vercel.json` configuration

## 📦 File Structure

```
.
├── app.py                  # Flask app
├── vercel.json            # Vercel configuration
├── requirements.txt       # Python dependencies
├── templates/
│   └── admin.html        # Admin panel UI
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## 🎉 Selamat!

Sekarang API update manager Anda sudah online dan bisa diakses dari mana saja!
