document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('quizSettingsForm');
    const startButton = document.getElementById('submitBtn');
    const errorMsg = document.getElementById('error-message');

    const checkValidity = () => {
        const kategorie = form.querySelector('[name="kategorie"]').value;
        const kontinent = form.querySelector('[name="kontinent"]').value;
        const levelChecked = form.querySelector('input[name="level"]:checked') !== null;

        if (kategorie && kontinent && levelChecked) {
            startButton.disabled = false;
            errorMsg.classList.add("hidden");
            errorMsg.classList.remove("visible");
        } else {
            startButton.disabled = true;
        }
    };

    form.addEventListener('input', checkValidity);
    form.addEventListener('submit', (e) => {
        if (startButton.disabled) {
            e.preventDefault();
            errorMsg.classList.remove("hidden");
            errorMsg.classList.add("visible");
        }
    });

    // Initial prüfen
    checkValidity();
});
