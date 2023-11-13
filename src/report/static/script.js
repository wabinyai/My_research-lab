// Example script for handling date pickers using a library like flatpickr
document.addEventListener('DOMContentLoaded', function () {
    flatpickr("#start_time", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
    });

    flatpickr("#end_time", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
    });
});

// Example script for making an AJAX request (using Fetch API)
document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();

    // Get form data
    const formData = new FormData(this);

    // Make an AJAX request
    fetch('/', {
        method: 'POST',
        body: formData,
        headers: {
            'Content-Type': 'application/json', // Add headers if required
        },
    })
        .then(response => response.json())
        .then(data => {
            // Handle the response data
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
