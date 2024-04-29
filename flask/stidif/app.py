import traceback
from flask import Flask, render_template, url_for, request, jsonify, redirect, session, Request
import jwt
from functools import wraps
from datetime import datetime, timedelta,timezone
import requests
import sub
import multiprocessing

app = Flask(__name__)


app.config['SECRET_KEY'] = 'secret_key'
users = {
    "admin@envisionsapp.com": {"password": "password"},
    "admin@stidif.com": {"password": "password"}
}

def generate_token(user_info):
    # payload = {
    #     'user_info': user_info,
    #     'exp': datetime.now(timezone.utc) + timedelta(days=1)
    # }
    # token = jwt.encode(payload, app.secret_key, algorithm='HS256')
    login_url = 'https://api2.envisionsapp.com/api/v1/login'
    locations_response = requests.post(login_url, data=user_info)
    data = locations_response.json()
    token = data['data']['accessToken']
    return token

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login_token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/token', methods=['POST'])
def get_token():
    data = request.get_json()
    user_info = data.get('user_info')
    if user_info:
        token = generate_token(user_info)
        return jsonify({'token': token.decode('utf-8')}), 200
    else:
        return jsonify({'error': 'User info is required'}), 400
    
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        api_login_data = {'email': email, 'password': password}
        response = requests.post('http://127.0.0.1:5000/api/login', json=api_login_data)
        if response.status_code == 200:
            token = response.json().get('token')
            session['login_token'] = token  # Simpan token dalam session
            return redirect(url_for('dashboard'))
        else:
            return 'Email atau password salah'
    return render_template('login.html')

@app.route('/api/login', methods=['GET', 'POST'])
def login_api():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Validasi kredensial
        if email in users and users[email]['password'] == password:
            user_info = {
                "email": email,
                "password": password
            }
            token = generate_token(user_info)  # Menghasilkan token
            return jsonify({'message': 'Login successful', 'token': token}), 200
        else:
            return jsonify({'message': 'Login failed. Invalid email or password'}), 401
    elif request.method == 'GET':
        # Penanganan permintaan GET
        return jsonify({'message': 'Metode ini tidak diperbolehkan'}), 405

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

def run_subscriber():
    sub.run()
# Data perangkat dari atribut JSON
# class1401_data = {
#     "id": "de6b0910-53a7-41e0-bc4e-1d535967f686",
#     "code": "TLKM-BDG-LT14-CLASS01",
#     "name": "Class-1401",
#     "last_data": {
#         "cctv_people": 5,
#         "cctv_status": True,
#         "3_gang_saklar1": False,
#         "3_gang_saklar2": True,
#         "3_gang_saklar3": False
#     }
# }

# @app.route('/class-1401', methods=['GET'])
# def class1401():
#     # Periksa apakah data berhasil diambil
#     if class1401_data:
#         return render_template('class-1401.html', class1401_data=class1401_data)
#     else:
#         return "Failed to fetch class1401 data", 500
    
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/control')
def control():
    return render_template('control.html')

@app.route('/logout')
def logout():
    # Hapus sesi pengguna di sini, contoh menggunakan session Flask
    session.pop('username', None)
    # Redirect pengguna ke halaman login atau halaman lain yang sesuai
    return redirect(url_for('login'))

from datetime import datetime

def format_datetime(dt_str):
    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.strftime("%d %B %Y")

TOKEN_KEY = 'eyJhbGciOiJSUzI1NiJ9.eyJkYXRhIjp7ImlkIjoiZDU3NGViZGQtMGM3NC00NmY0LWExNDktMjlhZTkwYjA5NDFkIiwibmFtZSI6ImFkbWluIiwiZW1haWwiOiJhZG1pbkB0ZWxrb211bml2ZXJzaXR5LmFjLmlkIiwiY29tcGFueSI6eyJpZCI6ImU4MGY5ZThkLTY5NDgtNDA0Zi1hOGRkLTA1NTNiZGEyYTY3NyIsIm5hbWUiOiJURUxLT00ifSwicGVybWlzc2lvbnMiOlsic2hvd19ob21lIiwic2hvd19wbHVnaW5fc3VydmV5Iiwic2hvd19zZXR0aW5nIiwic2hvd19wbHVnaW5fZW5lcmd5Iiwic2hvd19wbHVnaW5fcmVwb3J0Iiwic2hvd19wbHVnaW5fcm9vbV9yZXNlcnZhdGlvbl9kZWxldGUiLCJzaG93X3BsdWdpbl9yb29tX3Jlc2VydmF0aW9uX2V4cG9ydCIsInNob3dfcGx1Z2luX3Jvb21fcmVzZXJ2YXRpb25fY3JlYXRlIiwic2hvd19wbHVnaW5zIiwic2hvd19wbHVnaW5fY2N0dl9jb3VudGluZyIsInNob3dfcGx1Z2luX3Jvb21fcmVzZXJ2YXRpb25fdXBkYXRlIl0sInVzZXJJZCI6ImQ1NzRlYmRkLTBjNzQtNDZmNC1hMTQ5LTI5YWU5MGIwOTQxZCJ9LCJpYXQiOjE3MTM3NzU0NDAsImV4cCI6MTcxMzg2MTg0MH0.WEIvCmkcICKskwATQRzK53sfJmfCg3ryoj_4UBa093r_WljcBKbb2WguiS9DSGbP5utykXk3qtOppLWwqhXE00NXFPtRmj9IUY6Boi7FB0JMq5YaojK_ExOGXGeE3Oz5L4uat17IeKGF2RZ3GiyODvYTXMiJzMjqSth22idDbU9HXdfTe1HDr15qqMfugE2Fw7friPA6PNTXupJh26WMRDhePVkT5HAytNKKNJVOz3S0an8SXqgsdVV0qIpN5PXxL-f_NRiSIV377aWVGIYP8sJkARbeAeCIzAjtK688jn_n9YeKbLEcDGL-AWYY5sE-Cn27QF5yZUeWj1lfBZFeLBcV-b8UZSUVA2TKAEQvOr0DuVopMFZGFFZzFFCZrBndhvOjeUpHoPk1mjBO02GjelRDBSvm-pytZsS-gMijV112E8owbuT86TTHshjmE2XFD3ALm2-VAC9vWmUXzrxiq4aOwd9hkKChFZagqD21KhZwFLexod-fEOJc56hM1nEl0VcdnSWI4uQqV0h-3Y2eo4CkKcRrPVrDnDwXBWtCTf29jzlMfhCbEYxPWRHEjXbbvN4CKkI3ntjaOopVVYqKkS9KrEyQtP8k9l9DPZhvyswtBln6RqFM8LeVYU0-lMySSL4ZeoYEM-M05C593LFbfaNRrc8ggwZyfFYKE2YrWS0'




@app.route('/get_assets', methods=['GET'])
def get_assets():
    tokenLogin = request.args.get('token')
    # print(request.args)
    headers = {'Authorization': f'Bearer {tokenLogin}'}
    response = None  # Inisialisasi response dengan nilai default None
    try:
        # Ambil nilai dari pesan MQTT yang disimpan di variabel sub.mqtt_data
        mqtt_data = sub.mqtt_data

        status_on1 = mqtt_data.get('3_gang_saklar1', False)
        status_on2 = mqtt_data.get('3_gang_saklar2', False)
        status_on3 = mqtt_data.get('3_gang_saklar3', False)

        # Mengambil data locations
        locations_url = 'https://api2.envisionsapp.com/api/v1/locations'
        locations_response = requests.get(locations_url, headers=headers)
        locations_data = locations_response.json()

        # Mengambil id dari location pertama
        # print(locations_data)
        location_id = locations_data['data'][0]['id']

        # Mengambil data areas berdasarkan location_id
        areas_url = f'https://api2.envisionsapp.com/api/v1/areas?location_id={location_id}'
        areas_response = requests.get(areas_url, headers=headers)
        areas_data = areas_response.json()

        # Mengambil id dan name dari area pertama
        area_id = areas_data['data'][0]['id']
        area_name = areas_data['data'][0]['name']

        # Mengambil data assets berdasarkan area_id
        assets_url = f'https://api2.envisionsapp.com/api/v1/assets?area_id={area_id}'
        assets_response = requests.get(assets_url, headers=headers)
        assets_data = assets_response.json()
        # print('assett:',assets_data)

        # # Mengonversi updated_at ke format yang diinginkan
        for asset in assets_data['data']:
            asset['updated_at'] = format_datetime(asset['updated_at'])
        
        # print('updated_at')
        # print(assets_data['data'])
        # Memformat response
        response = {
            "location_id": location_id,
            "area_id": area_id,
            "area_name": area_name,
            "assets": assets_data['data']
        }

        # Cetak data assets
        # print("Data assets:")
        # for asset in response['assets']:
        #     print(asset)
        print('response')
        print(response)
        return render_template('class-1401.html', response=response, status_on1=status_on1, status_on2=status_on2, status_on3=status_on3)
    
    except requests.exceptions.RequestException as e:
        if response is not None:
            # Jika response sudah terisi, gunakan nilai response yang ada
            return render_template('class-1401.html', response=response, status_on1=status_on1, status_on2=status_on2, status_on3=status_on3)
        else:
            # Jika response belum terisi, kembalikan error
            return jsonify({"error": str(e)}), 500

        
import requests

@app.route('/controlProcces', methods=['POST'])
def controlProcces():
    idtenant = request.json.get('idtenant')
    iddevice = request.json.get('iddevice')
    name = request.json.get('name')  # Mendapatkan nilai 'name' dari JSON
    attribute = request.json.get('attribute')  # Mendapatkan nilai 'attribute' dari JSON
    data = request.json.get('data')  # Mendapatkan nilai 'data' dari JSON
    tokenLogin = request.json.get('token')
    if not all([name, attribute, data]):
        return jsonify({"error": "Incomplete data."}), 400

    try:
        # Menyiapkan payload untuk dikirim ke API
        payload = {
            'idtenant': idtenant,
            'iddevice': iddevice,
            'name': name,
            'attribute': attribute,
            'data': data
        }
        headers = {'Authorization': f'Bearer {tokenLogin}'}
        # Melakukan permintaan POST ke API dengan header dan payload yang disiapkan
        response = requests.post('https://api2.envisionsapp.com/iot/api/v1/control', headers=headers, json=payload)

        # Memeriksa status code respon dari API
        if response.status_code == 200:
            return jsonify({"message": "Data received successfully."}), 200
        else:
            return jsonify({"error": f"Failed to send data to API. Status code: {response.status_code}"}), 500

    except Exception as e:
        traceback.print_exc()  # Menampilkan traceback ke konsol Flask
        return jsonify({"error": "Internal server error."}), 500


if __name__ == '__main__':
    # Start MQTT subscriber di thread terpisah
    sub_process = multiprocessing.Process(target=run_subscriber)
    sub_process.start()
    app.run(debug=True)