// static/js/main.js
document.addEventListener('DOMContentLoaded', function () {
    var dashboardLink = document.getElementById('dashboard-link');
    var dashboardContent = document.getElementById('dashboard-content');

    // Tambahkan event listener untuk tindakan klik
    dashboardLink.addEventListener('click', function (event) {
        event.preventDefault(); // Mencegah perilaku default dari tautan

        // Tampilkan atau sembunyikan konten dashboard
        if (dashboardContent.style.display === 'none') {
            dashboardContent.style.display = 'block';
        } else {
            dashboardContent.style.display = 'none';
        }
    });
});

