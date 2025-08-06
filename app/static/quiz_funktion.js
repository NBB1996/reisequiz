document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll('.answer-option');
    const selectedAnswer = document.getElementById('selected_answer');
    const submitBtn = document.getElementById('submitBtn');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('selected-answer', 'btn-primary'));
            button.classList.add('selected-answer', 'btn-primary');
            selectedAnswer.value = button.dataset.value;
            submitBtn.disabled = false;
        });
    });

    document.getElementById('quizForm').addEventListener('submit', function(e) {
        if (!selectedAnswer.value) {
            e.preventDefault();  // Fallback-Schutz, falls etwas schiefläuft
        }
    });
});
