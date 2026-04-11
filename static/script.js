document.getElementById('form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = {};
    
    formData.forEach((value, key) => {
        data[key] = value;
    });

    console.log("Sending data:", data);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const text = await response.text();
        console.log("Response:", text);

        const result = JSON.parse(text);
        document.getElementById('career').textContent = result.orientation;
        document.getElementById('result').classList.remove('hidden');

    } catch (err) {
        console.error("Erreur:", err);
    }
});