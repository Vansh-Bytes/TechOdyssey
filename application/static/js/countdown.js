function updateTime() {
    let now = new Date();
    let targetDate = new Date("2024-04-25T00:00:00+05:30");

    let timeRemaining = targetDate - now;

    if (timeRemaining < 0) {
        // If the target date has passed, set time remaining to 0
        timeRemaining = 0;
    }

    let daysRemaining = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
    let hoursRemaining = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    let minutesRemaining = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
    let secondsRemaining = Math.floor((timeRemaining % (1000 * 60)) / 1000);

    document.getElementById("days").innerHTML = daysRemaining;
    document.getElementById("hours").innerHTML = hoursRemaining;
    document.getElementById("minutes").innerHTML = minutesRemaining;
    document.getElementById("seconds").innerHTML = secondsRemaining;

    console.log("Time remaining: " + daysRemaining + "d " + hoursRemaining + "h " + minutesRemaining + "m " + secondsRemaining + "s");

    setTimeout(updateTime, 1000);
}

document.addEventListener("DOMContentLoaded", function () {
    updateTime();
});
