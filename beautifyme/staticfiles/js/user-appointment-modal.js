document.getElementById("appointmentForm").addEventListener("submit", function (event) {
    event.preventDefault();

    var selectedDate = new Date(document.getElementById("appointment_date").value);

    var currentDate = new Date();

    if (selectedDate <= currentDate) {
        document.getElementById("date-error").style.display = "block";
    } else {
        document.getElementById("appointmentForm").submit();
    }
});