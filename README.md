# 📘 Tugas 1: API Sederhana dengan JWT (Flask)

Implementasi API sederhana menggunakan Python, Flask, dan Flask-JWT-Extended.

Proyek ini mencakup semua fitur wajib serta fitur bonus:
1.  **Fitur Wajib**: Login JWT, endpoint publik (`/items`), endpoint terproteksi (`/profile`).
2.  **Fitur Bonus**: Refresh token (`/auth/refresh`) dan Role-Based Access Control (RBAC) untuk endpoint admin (`/admin/users`).

---

## 1. Setup & Menjalankan Server

### Prasyarat
* Python 3.8+
* `pip` dan `venv`

### Langkah-langkah
1.  **Clone repositori** (atau salin file `app.py`, `requirements.txt`, `.env.example`).

2.  **Buat dan Aktifkan Virtual Environment (`venv`)**
    ```bash
    # 1. Buat venv
    python -m venv venv
    
    # 2. Aktifkan venv
    # Windows (Command Prompt / Git Bash)
    source venv/Scripts/activate
    # Windows (PowerShell)
    .\venv\Scripts\Activate.ps1
    # macOS / Linux
    source venv/bin/activate
    ```
    Anda akan melihat `(.venv)` di awal *prompt* terminal Anda.

3.  **Install Dependensi**
    Pastikan `requirements.txt` ada, lalu jalankan:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Buat File `.env`**
    Salin file `.env.example` menjadi file baru bernama `.env`.
    ```bash
    cp .env.example .env
    ```
    Buka file `.env` dan **wajib** isi nilai `JWT_SECRET` dengan string acak yang kuat.

5.  **Menjalankan Server**
    ```bash
    python app.py
    ```
    Server akan berjalan di `http://localhost:5000` (atau port yang Anda tentukan di `.env`). Biarkan terminal ini tetap berjalan.

---

## 2. Variabel Environment (`.env`)

File `.env` Anda harus berisi:

```ini
# Port server (default jika tidak ada: 5000)
PORT=5000

# Kunci rahasia untuk menandatangani JWT (WAJIB DIISI!)
JWT_SECRET=ganti_dengan_kunci_rahasia_anda_yang_sangat_panjang
```

### 3. Kredensial Demo

Semua pengguna berikut menggunakan password yang sama: **`pass123`**

| Nama      | Email                  | Role    |
| :-------- | :--------------------- | :------ |
| Admin     | `admin@gmail.com`      | `admin` |
| Ilham     | `ilham@gmail.com`      | `user`  |
| Fairuzia  | `fairuzia@gmail.com`   | `user`  |
| Hanif     | `hanif@gmail.com`      | `user`  |
| Syariel   | `syariel@gmail.com`    | `user`  |

## 4. Daftar Endpoint API

### 4.1 Autentikasi

#### `POST /auth/login`
(Publik) Login untuk mendapatkan `access_token` (15 menit) dan `refresh_token` (7 hari).

* **Body (JSON):**
    ```json
    {
      "email": "ilham@gmail.com",
      "password": "pass123"
    }
    ```
* **Respon Sukses (200):**
    ```json
    {
      "access_token": "<jwt_access_string_15m>",
      "refresh_token": "<jwt_refresh_string_7d>"
    }
    ```

#### `POST /auth/refresh` (Bonus)
(Terproteksi) Menggunakan `refresh_token` untuk mendapatkan `access_token` baru.

* **Header Wajib:** `Authorization: Bearer <REFRESH_TOKEN>`
* **Respon Sukses (200):**
    ```json
    {
      "access_token": "<jwt_access_string_baru_15m>"
    }
    ```

### 4.2 Marketplace

#### `GET /items` (Wajib)
(Publik) Mendapatkan daftar item.

* **Respon Sukses (200):**
    ```json
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
    ```

### 4.3 Profil Pengguna

#### `PUT /profile` (Wajib)
(Terproteksi) Memperbarui profil milik *user* yang sedang login.

* **Header Wajib:** `Authorization: Bearer <ACCESS_TOKEN>`
* **Body (JSON):** `{ "name": "Nama Baru" }`
* **Respon Sukses (200):** `{"message": "Profile updated", "profile": ...}`
* **Respon Gagal (401):** `{"error": "Access token expired"}`

### 4.4 Admin

#### `GET /admin/users` (Bonus)
(Terproteksi - Admin Only) Melihat semua *user* di sistem.

* **Header Wajib:** `Authorization: Bearer <ACCESS_TOKEN_ADMIN>`
* **Respon Sukses (200):** `{"users": [...]}`
* **Respon Gagal (403 Forbidden):** `{"error": "Admin access required"}`

## 5. Contoh Pengujian (cURL)

Buka **Terminal 2** (biarkan server berjalan di Terminal 1). Gunakan perintah cURL dalam **satu baris** untuk menghindari *error*.

### Skenario 1: Login & Dapatkan Token
Login sebagai *user* dan *admin* untuk mendapatkan token mereka.

* **Login sebagai Ilham (User)**
    ```bash
    # 1. Login sebagai Ilham (User)
    curl -s -X POST http://localhost:5000/auth/login -H "Content-Type: application/json" -d '{"email":"ilham@gmail.com","password":"pass123"}'
    ```
    * **Aksi:** Salin `access_token` dari output. Kita sebut `USER_TOKEN`.
    * **Aksi:** Salin `refresh_token` dari output. Kita sebut `USER_REFRESH`.

* **Login sebagai Admin**
    ```bash
    # 2. Login sebagai Admin
    curl -s -X POST http://localhost:5000/auth/login -H "Content-Type: application/json" -d '{"email":"admin@gmail.com","password":"pass123"}'
    ```
    * **Aksi:** Salin `access_token` dari output. Kita sebut `ADMIN_TOKEN`.

### Skenario 2: Set Variabel di Terminal (PENTING)
Tetapkan token ke variabel terminal agar mudah digunakan. (Ganti `...` dengan token yang Anda salin).

```bash
# Set token Ilham (User)
TOKEN="eyJhbGciOi...sZXIifQ.ZxMpiZ..."
REFRESH_TOKEN="eyJhbGciOi...x1ZBI_tpd9U"

# Set token Admin
ADMIN_TOKEN="eyJhbGciOi...NVUm4"



