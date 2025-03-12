async function fetchQuestions() {
    const response = await fetch('/questionList');
    const questions = await response.json();
    console.log(questions);
    return questions;
}

document.addEventListener('DOMContentLoaded', async () => {
    const questions = await fetchQuestions();
    generateForm(questions);
});

function generateForm(questions) {
    const form = document.createElement('form');

    for (const question of questions) {
        const label = document.createElement('label');
        label.textContent = question;
        const input = document.createElement('textarea');
        input.name = question;

        form.appendChild(label);
        form.appendChild(input);
        form.appendChild(document.createElement('br'));
    }

    const submitButton = document.createElement('button');
    submitButton.type = 'submit';
    submitButton.textContent = 'Submit';
    form.appendChild(submitButton);

    document.body.appendChild(form);
}

document.addEventListener('DOMContentLoaded', () => {
    generateForm(questions);
});