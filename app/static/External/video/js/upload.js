document.getElementById('video-upload-form').addEventListener('submit', function (e) {
    e.preventDefault();

    var formData = new FormData();
    formData.append('title', document.getElementById('video-title').value);
    formData.append('description', document.getElementById('video-description').value);
    formData.append('subject', document.getElementById('course-select').value);
    formData.append('file_path', document.getElementById('video-file').files[0]);

    fetch('/videos/create', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token() }}'  // Ensure CSRF token if using Flask-WTF
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById('video-upload-success').classList.remove('d-none');
        }
    })
    .catch(error => {
        document.getElementById('video-upload-error').classList.remove('d-none');
        console.error('Error:', error);
    });
});
