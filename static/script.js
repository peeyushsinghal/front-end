document.querySelectorAll('input[name="animal"]').forEach(radio => {
    radio.addEventListener('change', function() {
        const animal = this.value;
        fetch(`/get_animal_image/${animal}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('animalImage').innerHTML = `<img src="${data.image_url}" alt="${animal}">`;
            });
    });
});

function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a file first.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload_file', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('fileInfo').innerHTML = `
            <p>File Name: ${data.filename}</p>
            <p>File Size: ${data.size} bytes</p>
            <p>File Type: ${data.content_type}</p>
        `;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while uploading the file.');
    });
}
