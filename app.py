import os
import logging
from datetime import datetime, timedelta
from functools import wraps # Diperlukan untuk decorator kustom
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from flask_cors import CORS
from dotenv import load_dotenv
import bcrypt

# Muat variabel dari .env
load_dotenv()

# Konfigurasi logging ringkas
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

app = Flask(__name__)
CORS(app)  # Mengaktifkan CORS untuk semua route

# --- Konfigurasi Flask & JWT (Lengkap) ---
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7) # Fitur Bonus
jwt = JWTManager(app)

# --- Database In-Memory Sederhana (Sesuai Request Anda) ---
# Password 'pass123' untuk SEMUA user
shared_pass_hash = bcrypt.hashpw(b'pass123', bcrypt.gensalt()).decode('utf-8')

db_users = {
    # User 1: Admin
    "a001": {
        "id": "a001",
        "name": "Admin",
        "email": "admin@gmail.com",
        "password_hash": shared_pass_hash,
        "role": "admin"
    },
    # User 2: Ilham
    "u001": {
        "id": "u001",
        "name": "Ilham",
        "email": "ilham@gmail.com",
        "password_hash": shared_pass_hash,
        "role": "user"
    },
    # User 3: Fairuzia
    "u002": {
        "id": "u002",
        "name": "Fairuzia",
        "email": "fairuzia@gmail.com",
        "password_hash": shared_pass_hash,
        "role": "user"
    },
    # User 4: Hanif
    "u003": {
        "id": "u003",
        "name": "Hanif",
        "email": "hanif@gmail.com",
        "password_hash": shared_pass_hash,
        "role": "user"
    },
    # User 5: Syariel
    "u004": {
        "id": "u004",
        "name": "Syariel",
        "email": "syariel@gmail.com",
        "password_hash": shared_pass_hash,
        "role": "user"
    }
}

# Helper untuk mencari user berdasarkan email saat login
def find_user_by_email(email):
    for user in db_users.values():
        if user['email'] == email:
            return user
    return None

db_items = [
    {"id": 1, "name": "Action Figure (Limited)", "price": 1250000},
    {"id": 2, "name": "Vinyl Record (Classic Album)", "price": 450000},
    {"id": 3, "name": "Model Kit (Gundam MG)", "price": 800000},
    {"id": 4, "name": "Rare Trading Card (Single)", "price": 300000},
    {"id": 5, "name": "Board Game (Catan)", "price": 650000},
    {"id": 6, "name": "Kamera Analog (Bekas)", "price": 1500000},
    {"id": 7, "name": "Buku Komik (Edisi Pertama)", "price": 500000},
    {"id": 8, "name": "Fountain Pen (Premium)", "price": 2100000},
    {"id": 9, "name": "Sepatu Lari (Marathon)", "price": 1750000},
    {"id": 10, "name": "Skateboard Deck (Art)", "price": 900000}
]


# --- Penanganan Error JWT Kustom (Wajib) ---
@jwt.unauthorized_loader
def unauthorized_callback(reason):
    logging.warning(f"Unauthorized access attempt: {reason}")
    return jsonify({"error": "Missing or invalid Authorization header"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    logging.warning(f"Invalid token received: {error}")
    return jsonify({"error": "Invalid token"}), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    # Cek apakah token yang expired adalah access atau refresh token
    if jwt_payload.get('type') == 'refresh':
        return jsonify({"error": "Refresh token expired"}), 401
    logging.info("Expired token detected")
    return jsonify({"error": "Access token expired"}), 401


# --- Decorator Kustom untuk Role-Based Access (Fitur Bonus) ---
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required() # Pastikan token valid dulu
        def decorator(*args, **kwargs):
            claims = get_jwt() # Dapatkan payload/claims dari token
            if claims.get("role") == "admin":
                return fn(*args, **kwargs) # Lanjutkan jika admin
            else:
                logging.warning(f"Forbidden: User {get_jwt_identity()} (role: {claims.get('role')}) tried to access admin route.")
                return jsonify({"error": "Admin access required"}), 403 # 403 Forbidden
        return decorator
    return wrapper


# === ENDPOINTS ===

# 1. POST /auth/login (Diperbarui untuk Refresh Token)
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = find_user_by_email(email)

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        # Buat claims, tambahkan 'role'
        additional_claims = {
            "email": user["email"],
            "role": user["role"]
        }
        
        # Buat access token (15 menit)
        access_token = create_access_token(
            identity=user["id"], 
            additional_claims=additional_claims
        )
        
        # Buat refresh token (7 hari)
        refresh_token = create_refresh_token(
            identity=user["id"],
            additional_claims=additional_claims
        )
        
        logging.info(f"Login success for user: {email} (Role: {user['role']})")
        
        # Kirim KEDUA token
        return jsonify(
            access_token=access_token,
            refresh_token=refresh_token 
        ), 200
    else:
        logging.warning(f"Invalid login attempt for: {email}")
        return jsonify({"error": "Invalid credentials"}), 401

# 2. POST /auth/refresh (Endpoint Bonus Baru)
@app.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True) 
def refresh():
    current_user_id = get_jwt_identity()
    user = db_users.get(current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Ambil claims dari refresh token untuk dimasukkan ke access token baru
    old_claims = get_jwt()
    new_claims = {
        "email": old_claims.get("email"),
        "role": old_claims.get("role")
    }

    # Buat HANYA access token baru
    new_access_token = create_access_token(
        identity=current_user_id,
        additional_claims=new_claims
    )
    
    logging.info(f"Access token refreshed for user ID: {current_user_id}")
    return jsonify(access_token=new_access_token), 200

# 3. GET /items (Publik - Wajib)
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items=db_items), 200

# 4. PUT /profile (Terproteksi - Wajib)
@app.route('/profile', methods=['PUT'])
@jwt_required() # Terproteksi oleh access token
def update_profile():
    current_user_id = get_jwt_identity() 
    user = db_users.get(current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if 'name' not in data and 'email' not in data:
        return jsonify({"error": "At least one field (name or email) is required"}), 400

    if 'name' in data: user['name'] = data['name']
    if 'email' in data: user['email'] = data['email']
    
    logging.info(f"Profile updated for user ID: {current_user_id}")
    
    return jsonify(
        message="Profile updated",
        profile={"name": user["name"], "email": user["email"]}
    ), 200

# 5. GET /admin/users (Endpoint Bonus Baru)
@app.route('/admin/users', methods=['GET'])
@admin_required() # Menggunakan decorator kustom
def get_all_users():
    admin_id = get_jwt_identity()
    logging.info(f"Admin access granted for: {admin_id}")
    
    # Siapkan daftar user (jangan sertakan hash password)
    user_list = [
        {"id": u["id"], "name": u["name"], "email": u["email"], "role": u["role"]} 
        for u in db_users.values()
    ]
    return jsonify(users=user_list), 200

# --- Menjalankan Server ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # Gunakan debug=True untuk development agar server auto-reload
    app.run(host='0.0.0.0', port=port, debug=True)