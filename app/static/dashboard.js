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

document.getElementById('add-course-form').addEventListener('submit', async function (event) {
    event.preventDefault();
    
    const courseName = document.getElementById('course-name').value;
    const courseDescription = document.getElementById('course-description').value;

    const response = await fetch('/courses/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: courseName, description: courseDescription })
    });

    const data = await response.json();
    if (response.ok) {
        document.getElementById('add-course-success').innerText = data.message;
        document.getElementById('add-course-success').classList.remove('d-none');
        document.getElementById('course-name').value = ''; 
        document.getElementById('course-description').value = ''; 
        document.getElementById('add-course-modal').style.display = 'none';  // Close the modal
    } else {
        document.getElementById('add-course-error').innerText = data.message;
        document.getElementById('add-course-error').classList.remove('d-none');
    }
});
