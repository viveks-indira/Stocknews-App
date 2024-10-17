// Common JavaScript functionality for the application

// Document ready event
document.addEventListener('DOMContentLoaded', function () {
    console.log("JavaScript loaded successfully.");

    // Form submission event for the screenshot upload form
    const uploadForm = document.querySelector('form[action*="upload_file"]');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function (e) {
            // Perform validation or any pre-processing here
            const input = uploadForm.querySelector('input[type="file"]');
            if (input.files.length === 0) {
                e.preventDefault();
                alert("Please select at least one file to upload.");
            }
        });
    }

    // Form submission event for fetching news from URL
    const urlForm = document.querySelector('form[action*="url_generation"]');
    if (urlForm) {
        urlForm.addEventListener('submit', function (e) {
            // Simple URL validation
            const urlInput = urlForm.querySelector('input[name="url"]');
            const urlPattern = /^(ftp|http|https):\/\/[^ "]+$/;
            if (!urlPattern.test(urlInput.value)) {
                e.preventDefault();
                alert("Please enter a valid URL.");
            }
        });
    }
});
