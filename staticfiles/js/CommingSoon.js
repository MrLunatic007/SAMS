// Set the date we're counting down to
const countDownDate = new Date("Mar 1, 2025 00:00:00").getTime();

// Update the countdown every 1 second
const countdownInterval = setInterval(function() {

    // Get current date and time
    const now = new Date().getTime();
    
    // Calculate the time left
    const distance = countDownDate - now;
    
    // Time calculations
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Display the result in the element with id="countdown"
    document.getElementById("countdown").innerHTML = `Launch in: ${days}d ${hours}h ${minutes}m ${seconds}s`;

    // If the countdown is finished, display a message
    if (distance < 0) {
        clearInterval(countdownInterval);
        document.getElementById("countdown").innerHTML = "We are live!";
    }
}, 1000);
