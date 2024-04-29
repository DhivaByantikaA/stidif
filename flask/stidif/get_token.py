import requests

url = 'http://localhost:5000/api/token'
headers = {'Content-Type': 'application/json'}
data = {'email': 'admin@stidif.com', 'password': 'password'}
response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    token = response.json().get('token')  # Mengambil token dari respons JSON
    print("Token API:", token)
else:
    print("Failed to get token:", response.text)

