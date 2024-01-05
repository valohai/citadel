const runningCb = document.getElementById("running");
const timeInput = document.getElementById("seconds");
const timerDiv = document.getElementById("timer-output");
function tick() {
  if (!runningCb.checked) return;
  const timeLeft = (timeInput.valueAsNumber = Math.round(
    Math.max(0, timeInput.valueAsNumber - 1),
  ));
  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;
  document.body.classList.toggle("out-of-time", timeLeft <= 0);
  timerDiv.innerHTML = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
  var scale = 1;
  if (timeLeft <= 60) {
    scale += (60 - timeLeft) / 30;
  }
  timerDiv.style.transform = `scale(${scale})`;
}
setInterval(tick, 1000);
