document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const files = document.getElementById('imageFile').files;

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const reader = new FileReader();

        reader.onload = function(event) {
            if (event.target.result) {  // Check if reading was successful
                const base64Image = event.target.result.split(",")[1];
                formData.append("image", base64Image);
                sendImage(formData);
            } else {
                console.error("Error reading file:", file);
            }
        };

        reader.readAsDataURL(file);
    }
});
port = process.env.BE_EP
function sendImage(data) {
    const baseUrl = window.location.origin
    fetch(`${port}/upload`, {
        method: 'POST',
        body: data
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerHTML = `Processing Outcome: ${data.message}`;
        // Additional code to display a comment box here
    })
    .catch(error => console.error(error));
}