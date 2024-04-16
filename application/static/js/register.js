const amountReference = {
    "0": 150,
    "1": 200,
    "2": 100,
    "3": 100,
    "4": 400,
    "5": 400,
    "6": 400,
};

function updateRegistration() {
    const selectedEvent = document.getElementById("event-id").value;
    const amount = selectedEvent ? amountReference[selectedEvent] : 0;
    document.getElementById("registration_amount").innerHTML = amount;

    const teamDetails = document.getElementById("team-details");
    teamDetails.style.display = selectedEvent === "4" || selectedEvent === "5" || selectedEvent === "6" ? "flex" : "none";
}

function register() {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const event = document.getElementById("event-id").value;
    const teamName = document.getElementById("team-name").value.trim();
    const teamMembers = document.getElementById("team_member_emails").value.trim();
    const paymentScreenshot = document.getElementById("payment-screenshot").files[0];
    const paymentTransactionId = document.getElementById("payment-transaction-id").value.trim();

    if (!name || !email || !event) {
        alert("Please fill in the required fields: Name, Email, Event");
        return;
    }

    if (["4", "5", "6"].includes(event) && (!teamName || !teamMembers)) {
        alert("Please fill in the required fields: Team Name, Team Members");
        return;
    }

    if (["4", "5", "6"].includes(event) && teamMembers.split(",").length !== (event === "4" ? 5 : 4)) {
        alert(`To participate in ${event === "4" ? "Battle Blitz: Valorant" : "Battle Blitz: PUBG Mobile or Battle Blitz: Free Fire"}, you need to have ${event === "4" ? 5 : 4} members in your team`);
        return;
    }

    if (!paymentScreenshot) {
        alert("Please upload the payment screenshot");
        return;
    }

    if (!paymentTransactionId) {
        alert("Please enter the payment transaction ID");
        return;
    }

    const formData = new FormData();
    formData.append("name", name);
    formData.append("email", email);
    formData.append("event", event);
    formData.append("teamName", teamName);
    formData.append("teamMembers", teamMembers);
    formData.append("paymentScreenshot", paymentScreenshot);
    formData.append("paymentTransactionId", paymentTransactionId);

    const registerButton = document.getElementById("register-button");
    registerButton.disabled = true;
    registerButton.innerHTML = "Registering...";

    fetch("/api/v1/register", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            window.location.href = "/user/events";
        } else {
            alert(data.message);
        }
    })
    .catch(() => {
        alert("Oops! Something went wrong. Please try again later");
    })
    .finally(() => {
        registerButton.disabled = false;
        registerButton.innerHTML = "Register";
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    const event = urlParams.get("event");

    if (event) {
        const eventReference = {
            "code-clash": "0",
            "web-dash": "1",
            "treasure-quest": "2",
            "reel-craft": "3",
            "battle-blitz": "4",
        };

        const eventId = eventReference[event];
        if (eventId !== null) {
            document.getElementById("event-id").value = eventId;
            updateRegistration();
        }
    }
});
