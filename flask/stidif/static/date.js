function updateDate() {
    var now = new Date();
    var year = now.getFullYear();
    var month = now.getMonth() + 1; // Bulan dimulai dari 0, tambahkan 1 untuk mendapatkan bulan yang benar
    var day = now.getDate();

    var dateString = padZero(day) + "/" + padZero(month) + "/" + year;
    document.getElementById('date').textContent = dateString;
}

function padZero(number) {
    return (number < 10 ? '0' : '') + number;
}

setInterval(updateDate, 1000);
