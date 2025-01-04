document.getElementById('reservationForm').addEventListener('submit', function (event) {
    const form = event.target;

    // Clear previous error messages
    document.querySelectorAll('.error-message').forEach(el => el.remove());

    let isValid = true;

    // Validate email
    const emailInput = form.querySelector('#reservation_email');
    if (!/^[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/.test(emailInput.value)) {
        showError(emailInput, 'Please enter a valid email address.');
        isValid = false;
    }

    // Validate reservation date
    const dateInput = form.querySelector('#reservation_date');
    const currentDate = new Date().toISOString().split('T')[0];
    if (dateInput.value && (dateInput.value < currentDate || dateInput.value > addYearsToToday(1))) {
        showError(dateInput, 'Reservation date must be within the next year.');
        isValid = false;
    }

    if (!isValid) {
        event.preventDefault();
    }
});

function showError(input, message) {
    const error = document.createElement('div');
    error.className = 'error-message';
    error.textContent = message;
    input.insertAdjacentElement('afterend', error);
}

function addYearsToToday(years) {
    const futureDate = new Date();
    futureDate.setFullYear(futureDate.getFullYear() + years);
    return futureDate.toISOString().split('T')[0];
}
