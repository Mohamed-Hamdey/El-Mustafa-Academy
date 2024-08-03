// Sidebar Menu Activation
const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

allSideMenu.forEach(item => {
    const li = item.parentElement;

    item.addEventListener('click', function () {
        allSideMenu.forEach(i => {
            i.parentElement.classList.remove('active');
        });
        li.classList.add('active');
    });
});

// Toggle Sidebar
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
    sidebar.classList.toggle('hide');
});

// Search Button Toggle
const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
    if (window.innerWidth < 576) {
        e.preventDefault();
        searchForm.classList.toggle('show');
        if (searchForm.classList.contains('show')) {
            searchButtonIcon.classList.replace('bx-search', 'bx-x');
        } else {
            searchButtonIcon.classList.replace('bx-x', 'bx-search');
        }
    }
});

// Responsive Behavior
if (window.innerWidth < 768) {
    sidebar.classList.add('hide');
} else if (window.innerWidth > 576) {
    searchButtonIcon.classList.replace('bx-x', 'bx-search');
    searchForm.classList.remove('show');
}

window.addEventListener('resize', function () {
    if (this.innerWidth > 576) {
        searchButtonIcon.classList.replace('bx-x', 'bx-search');
        searchForm.classList.remove('show');
    }
});

// Dark Mode Toggle
const switchMode = document.getElementById('switch-mode');

switchMode.addEventListener('change', function () {
    if (this.checked) {
        document.body.classList.add('dark');
    } else {
        document.body.classList.remove('dark');
    }
});

// Video Upload Functionality
document.getElementById('upload-video-btn').addEventListener('click', function () {
    document.getElementById('upload-video-modal').style.display = 'block';
});

document.querySelector('.close').addEventListener('click', function () {
    document.getElementById('upload-video-modal').style.display = 'none';
});

document.getElementById('upload-video-form').addEventListener('submit', async function (event) {
    event.preventDefault();
    const title = document.getElementById('video-title').value;
    const description = document.getElementById('video-description').value;
    const url = document.getElementById('video-url').value;
    const course_id = document.getElementById('video-course').value;

    const response = await fetch('/videos/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title, description, url, course_id })
    });

    const data = await response.json();
    if (response.ok) {
        alert(data.message);
        document.getElementById('upload-video-modal').style.display = 'none';
        loadVideos();  // Refresh the video list
    } else {
        document.getElementById('upload-error').innerText = data.message;
        document.getElementById('upload-error').classList.remove('d-none');
    }
});

// Function to load videos
async function loadVideos() {
    const response = await fetch('/videos');
    const videos = await response.json();
    const videoList = document.getElementById('video-list');
    videoList.innerHTML = '';

    videos.forEach(video => {
        const li = document.createElement('li');
        li.innerHTML = `<h3>${video.title}</h3><p>${video.description}</p><a href="${video.url}" target="_blank">Watch</a>`;
        videoList.appendChild(li);
    });
}

// Load videos when the page is loaded
window.onload = loadVideos;

// Redirect to video section
document.getElementById('videos-section').addEventListener('click', function () {
    window.location.href = "#video-list";  // Scroll to video list section
});

// Course Upload Form
document.getElementById('course-upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = new FormData();
    formData.append('title', document.getElementById('course-title').value);
    formData.append('description', document.getElementById('course-description').value);
    formData.append('subject', document.getElementById('course-subject').value);
    formData.append('stage', document.getElementById('course-stage').value);
    formData.append('file', document.getElementById('course-file').files[0]);

    fetch('/api/courses', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to upload course');
        }
    })
    .then(data => {
        alert('Course uploaded successfully');
        $('#uploadCourseModal').modal('hide');
        addCourseToList(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading course');
    });
});

function addCourseToList(course) {
    const courseList = document.getElementById('courses-list');
    const courseItem = document.createElement('li');
    courseItem.className = 'list-group-item';
    courseItem.textContent = `${course.title} - ${course.description}`;
    courseList.appendChild(courseItem);
}

// Assignments Upload Form
document.getElementById('assignments-upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('title', document.getElementById('assignment-title').value);
    formData.append('description', document.getElementById('assignment-description').value);
    formData.append('subject', document.getElementById('assignment-course-select').value);
    formData.append('stage', document.getElementById('assignment-stage-select').value);
    formData.append('file_path', document.getElementById('assignment-file').files[0]);

    try {
        const response = await fetch('/assignments', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrf-token]').content
            }
        });

        if (response.ok) {
            document.getElementById('assignment-upload-success').classList.remove('d-none');
            document.getElementById('assignment-upload-error').classList.add('d-none');
        } else {
            throw new Error('Failed to upload assignment');
        }
    } catch (error) {
        document.getElementById('assignment-upload-error').classList.remove('d-none');
        document.getElementById('assignment-upload-success').classList.add('d-none');
    }
});

// Exam Upload Form
document.getElementById('exam-upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = new FormData();
    formData.append('title', document.getElementById('exam-title').value);
    formData.append('description', document.getElementById('exam-description').value);
    formData.append('subject', document.getElementById('exam-subject').value);
    formData.append('stage', document.getElementById('exam-stage').value);

    let questions = [];
    document.querySelectorAll('.question-group').forEach(group => {
        let question = {
            question_text: group.querySelector('.question-text').value,
            correct_answer: group.querySelector('.correct-answer').value,
            choices: Array.from(group.querySelectorAll('.choice-text'), choiceInput => choiceInput.value)
        };
        questions.push(question);
    });
    formData.append('questions', JSON.stringify(questions));

    fetch('/api/exams', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to upload exam');
        }
    })
    .then(data => {
        alert('Exam uploaded successfully');
        $('#uploadExamModal').modal('hide');
        window.location.reload();
    })
    .catch(error => {
        alert(error.message);
    });
});

// Add Question Button
document.querySelector('.add-question-btn').addEventListener('click', function() {
    let questionGroup = document.querySelector('.question-group').cloneNode(true);
    questionGroup.querySelectorAll('input').forEach(input => input.value = '');
    document.getElementById('questions-section').appendChild(questionGroup);
});

// Add Choice Button
document.querySelector('.add-choice-btn').addEventListener('click', function() {
    let choiceInput = document.createElement('input');
    choiceInput.setAttribute('type', 'text');
    choiceInput.setAttribute('class', 'form-control choice-text');
    choiceInput.setAttribute('placeholder', 'Enter choice');
    this.parentNode.insertBefore(choiceInput, this);
});

// Handle Form Submission for Category Files
document.getElementById('category-files-upload-form').addEventListener('submit', function (e) {
    e.preventDefault();

    // Check that a category is selected
    const category = document.getElementById('category-file-select').value;
    if (!category) {
        alert('Please select a category.');
        return;
    }

    // Simulate file upload logic
    let success = true; // Simulate success or failure
    if (success) {
        document.getElementById('category-file-upload-success').classList.remove('d-none');
        document.getElementById('category-file-upload-error').classList.add('d-none');
    } else {
        document.getElementById('category-file-upload-error').classList.remove('d-none');
        document.getElementById('category-file-upload-success').classList.add('d-none');
    }
});

function openNewWindow(username, email, userId) {
    const newWindow = window.open("", "_blank", "width=400,height=300");

    if (newWindow) {
        newWindow.document.write(`
            <html>
            <head>
                <title>Request Details</title>
                <style>
                    .request-bar {
                        padding: 10px;
                        background-color: #f0f0f0;
                        border-bottom: 1px solid #ccc;
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                    }
                    .request-name {
                        font-weight: bold;
                    }
                    .buttons {
                        display: flex;
                        gap: 10px;
                    }
                    button {
                        padding: 5px 10px;
                        cursor: pointer;
                    }
                </style>
            </head>
            <body>
                <div class="request-bar">
                    <span class="request-name">${username} (${email})</span>
                    <div class="buttons">
                        <button onclick="handleAccept(${userId})">Accept</button>
                        <button onclick="handleReject(${userId})">Reject</button>
                    </div>
                </div>
                <script>
                    function handleAccept(userId) {
                        fetch('/handle_request/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ user_id: userId, action: 'accept' })
                        })
                        .then(response => response.json())
                        .then(data => {
                            alert(data.message);
                            window.close();
                            opener.location.reload(); // Refresh the parent window
                        })
                        .catch(error => console.error('Error:', error));
                    }

                    function handleReject(userId) {
                        fetch('/handle_request/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ user_id: userId, action: 'reject' })
                        })
                        .then(response => response.json())
                        .then(data => {
                            alert(data.message);
                            window.close();
                            opener.location.reload(); // Refresh the parent window
                        })
                        .catch(error => console.error('Error:', error));
                    }
                </script>
            </body>
            </html>
        `);
    } else {
        alert('Popup blocked. Please allow popups for this website.');
    }
}
