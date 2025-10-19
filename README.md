📘 Tugas 1: API Sederhana dengan JWT (Flask)

Versi Lengkap (Wajib + Bonus)

Implementasi API sederhana menggunakan Python, Flask, dan Flask-JWT-Extended.

Proyek ini mencakup semua fitur wajib serta fitur bonus:

Fitur Wajib: Login JWT, endpoint publik (/items), endpoint terproteksi (/profile).

Fitur Bonus: Refresh token (/auth/refresh) dan Role-Based Access Control (RBAC) untuk endpoint admin (/admin/users).

1. Setup & Menjalankan Server

Prasyarat

Python 3.8+

pip dan venv

Langkah-langkah

Clone repositori (atau salin file app.py, requirements.txt, .env.example).

Buat dan Aktifkan Virtual Environment (venv)

# 1. Buat venv
python -m venv venv

# 2. Aktifkan venv
# Windows (Command Prompt / Git Bash)
source venv/Scripts/activate
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate


Anda akan melihat (.venv) di awal prompt terminal Anda.

Install Dependensi
Pastikan requirements.txt ada, lalu jalankan:

pip install -r requirements.txt


Buat File .env
Salin file .env.example menjadi file baru bernama .env.

cp .env.example .env


Buka file .env dan wajib isi nilai JWT_SECRET dengan string acak yang kuat.

Menjalankan Server

python app.py


Server akan berjalan di http://localhost:5000 (atau port yang Anda tentukan di .env). Biarkan terminal ini tetap berjalan.

2. Variabel Environment (.env)

File .env Anda harus berisi:

# Port server (default jika tidak ada: 5000)
PORT=5000

# Kunci rahasia untuk menandatangani JWT (WAJIB DIISI!)
JWT_SECRET=ganti_dengan_kunci_rahasia_anda_yang_sangat_panjang


3. Kredensial Demo

Semua pengguna berikut menggunakan password yang sama: pass123

Nama

Email

Role

Admin

admin@gmail.com

admin

Ilham

ilham@gmail.com

user

Fairuzia

fairuzia@gmail.com

user

Hanif

hanif@gmail.com

user

Syariel

syariel@gmail.com

user

4. Daftar Endpoint API

4.1 Autentikasi

POST /auth/login

(Publik) Login untuk mendapatkan access_token (15 menit) dan refresh_token (7 hari).

Body (JSON):

{ "email": "ilham@gmail.com", "password": "pass123" }


Respon Sukses (200):

{
  "access_token": "<jwt_access_string_15m>",
  "refresh_token": "<jwt_refresh_string_7d>"
}


POST /auth/refresh (Bonus)

(Terproteksi) Menggunakan refresh_token untuk mendapatkan access_token baru.

Header Wajib: Authorization: Bearer <REFRESH_TOKEN>

Respon Sukses (200):

{ "access_token": "<jwt_access_string_baru_15m>" }


4.2 Marketplace

GET /items (Wajib)

(Publik) Mendapatkan daftar item.

Respon Sukses (200):

{
  "items": [
    { "id": 1, "name": "Action Figure (Limited)", "price": 1250000 },
    { "id": 2, "name": "Vinyl Record (Classic Album)", "price": 450000 },
    { "id": 3, "name": "Model Kit (Gundam MG)", "price": 800000 },
    { "id": 4, "name": "Rare Trading Card (Single)", "price": 300000 },
    { "id": 5, "name": "Board Game (Catan)", "price": 650000 },
    { "id": 6, "name": "Kamera Analog (Bekas)", "price": 1500000 },
    { "id": 7, "name": "Buku Komik (Edisi Pertama)", "price": 500000 },
    { "id": 8, "name": "Fountain Pen (Premium)", "price": 2100000 },
    { "id": 9, "name": "Sepatu Lari (Marathon)", "price": 1750000 },
    { "id": 10, "name": "Skateboard Deck (Art)", "price": 900000 }
  ]
}


4.3 Profil Pengguna

PUT /profile (Wajib)

(Terproteksi) Memperbarui profil milik user yang sedang login.

Header Wajib: Authorization: Bearer <ACCESS_TOKEN>

Body (JSON): { "name": "Nama Baru" }

Respon Sukses (200): {"message": "Profile updated", "profile": ...}

Respon Gagal (401): {"error": "Access token expired"}

4.4 Admin

GET /admin/users (Bonus)

(Terproteksi - Admin Only) Melihat semua user di sistem.

Header Wajib: Authorization: Bearer <ACCESS_TOKEN_ADMIN>

Respon Sukses (200): {"users": [...]}

Respon Gagal (403 Forbidden): {"error": "Admin access required"}

5. Contoh Pengujian (cURL)

Buka Terminal 2 (biarkan server berjalan di Terminal 1). Gunakan perintah cURL dalam satu baris untuk menghindari error.

Skenario 1: Login & Dapatkan Token

Login sebagai user dan admin untuk mendapatkan token mereka.

# 1. Login sebagai Ilham (User)
curl -s -X POST http://localhost:5000/auth/login -H "Content-Type: application/json" -d '{"email":"ilham@gmail.com","password":"pass123"}'

# 2. Login sebagai Admin
curl -s -X POST http://localhost:5000/auth/login -H "Content-Type: application/json" -d '{"email":"admin@gmail.com","password":"pass123"}'


Aksi: Salin access_token dan refresh_token dari output setiap login untuk digunakan di skenario berikutnya.

Skenario 2: Set Variabel di Terminal (Opsional, tapi Direkomendasikan)

Tetapkan token ke variabel terminal agar mudah digunakan. (Ganti ... dengan token yang Anda salin).

# Set token Ilham (User)
TOKEN="eyJhbGciOi...sZXIifQ.ZxMpiZ..."
REFRESH_TOKEN="eyJhbGciOi...x1ZBI_tpd9U"

# Set token Admin
ADMIN_TOKEN="eyJhbGciOi...NVUm4"


Skenario 3: Tes Endpoint Wajib

# 3.1. Get Items (Publik - Sukses)
curl -s http://localhost:5000/items

# 3.2. Update Profile (User - Sukses)
curl -s -X PUT http://localhost:5000/profile -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"name":"Ilham Keren"}'

# 3.3. Tes Tanpa Token (Gagal 401 - Missing)
curl -i -s -X PUT http://localhost:5000/profile -H "Content-Type: application/json" -d '{"name":"Gagal"}'

# 3.4. Tes Token Palsu (Gagal 401 - Invalid)
curl -i -s -X PUT http://localhost:5000/profile -H "Authorization: Bearer tokenpalsu123" -H "Content-Type: application/json" -d '{"name":"Gagal"}'

# 3.5. Tes Token Expired (Gagal 401 - Expired)
# (Tunggu 15 menit, lalu jalankan lagi perintah 3.2)
# Output yang diharapkan: {"error": "Access token expired"}


Skenario 4: Tes Endpoint Bonus

# 4.1. Refresh Token (Bonus - Sukses)
# (Jalankan ini setelah token di 3.5 expired)
curl -s -X POST http://localhost:5000/auth/refresh -H "Authorization: Bearer $REFRESH_TOKEN"
# Output: {"access_token": "<token_baru>"}

# 4.2. Coba Akses Admin (sebagai User - Gagal 403)
curl -i -s http://localhost:5000/admin/users -H "Authorization: Bearer $TOKEN"
# Output: HTTP/1.1 403 FORBIDDEN {"error": "Admin access required"}

# 4.3. Akses Admin (sebagai Admin - Sukses 200)
curl -s http://localhost:5000/admin/users -H "Authorization: Bearer $ADMIN_TOKEN"
# Output: {"users": [{"email": "admin@gmail.com", ...}, ...]}
