function updateClock() {
  var now = new Date();
  var hours = now.getHours();
  var minutes = now.getMinutes();
  var seconds = now.getSeconds();
  var timeString = padZero(hours) + ":" + padZero(minutes) + ":" + padZero(seconds);
  document.getElementById('clock').textContent = timeString;
}

function padZero(number) {
  return (number < 10 ? '0' : '') + number;
}

setInterval(updateClock, 1000);
