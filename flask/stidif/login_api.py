import requests

# Data kredensial pengguna
credentials = {
    "email": "admin@stidif.com",
    "password": "password"
}

# Endpoint login API
login_endpoint = 'http://127.0.0.1:5000/api/login'

# Kirim permintaan login dengan metode POST
response = requests.post(login_endpoint, json=credentials)

# Periksa respons
print(response.text)

# Periksa status kode tanggapan
if response.status_code == 200:
    try:
        # Cobalah untuk mengurai JSON dari tanggapan
        data = response.json()
        if 'token' in data:
            token = data['token']
            print("Login berhasil. Token JWT:", token)
        else:
            print("Tidak ada token dalam respons:", data)
    except Exception as e:
        # Tanggapan tidak berisi data JSON yang diharapkan
        print("Gagal mendapatkan token. Tanggapan server:", response.text)
else:
    # Login gagal
    print("Login gagal. Status code:", response.status_code)
