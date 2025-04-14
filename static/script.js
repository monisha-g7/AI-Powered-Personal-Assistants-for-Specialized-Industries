document.getElementById('textForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const domain = document.getElementById('domain').value;
    const question = document.getElementById('question').value;

    const formData = new FormData();
    formData.append('domain', domain);
    formData.append('question', question);

    const responseBox = document.getElementById('textResponse');
    responseBox.style.display = 'block';
    responseBox.innerHTML = 'Thinking...';

    const res = await fetch('/ask', {
        method: 'POST',
        body: formData
    });

    const data = await res.json();
    responseBox.innerHTML = '<strong>Assistant:</strong> ' + data.response;
});
