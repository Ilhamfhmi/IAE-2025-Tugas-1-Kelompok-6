# 📘 Tugas 1: API Sederhana dengan JWT (Flask)
# Versi Lengkap (Wajib + Bonus)

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



