function submitForm() {
    // Collect form data
    const form = document.getElementById('prediction-form');
    const formData = new FormData(form);
    const data = {};

    // Convert FormData to a plain object
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }

    // Send the data to the server
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        // Display the prediction result
        document.getElementById('result').innerText = `Prediction: ${result.prediction}`;
    })
    .catch(error => console.error('Error:', error));
}
