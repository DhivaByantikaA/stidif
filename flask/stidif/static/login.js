document.addEventListener('DOMContentLoaded', function() {
    // Menangkap formulir login
    const loginForm = document.getElementById('loginForm');

    // Menambahkan event listener untuk tindakan pengiriman formulir
    loginForm.addEventListener('submit', function(event) {
        // Mencegah perilaku default pengiriman formulir
        event.preventDefault();

        // Mendapatkan nilai email dan password dari formulir
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Membuat data objek untuk dikirim ke server
        const data = {
            email: email,
            password: password
        };

        // Mengirim permintaan login ke server menggunakan fetch API
        fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('diatas')
            console.log(data);
            localStorage.setItem('loginToken', data.token); // kode ini buat nyimpan token di local storage dengan nama login token, bisa diakses di inspect bagian application - local storage, setItem untuk nyimpan, getItem untuk dipake
            window.location.href = '/dashboard';
        })
        .catch(error => {
            console.error('Error:', error);
            // Tangani kesalahan jika terjadi
        });
    });
});

fetch('/api/class1401')
  .then(response => response.json())
  .then(data => {
    // Menampilkan data di halaman web
    document.getElementById('class1401Name').textContent = data.name;
    document.getElementById('cctvPeople').textContent = data.last_data.cctv_people;
    document.getElementById('cctvStatus').textContent = data.last_data.cctv_status ? 'Online' : 'Offline';
    document.getElementById('saklar1Status').textContent = data.last_data['3_gang_saklar1'] ? 'On' : 'Off';
    document.getElementById('saklar2Status').textContent = data.last_data['3_gang_saklar2'] ? 'On' : 'Off';
    document.getElementById('saklar3Status').textContent = data.last_data['3_gang_saklar3'] ? 'On' : 'Off';
  })
  .catch(error => console.error('Error:', error));