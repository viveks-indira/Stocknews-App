$(document).ready(function() {
    // Display the selected file name and preview the image if it's an image
    $('#fileInput').change(function(event) {
        var file = event.target.files[0];
        var fileName = file ? file.name : 'No file chosen yet';
        $('#filePreview p').text(fileName);

        // Check if the selected file is an image and preview it
        if (file && file.type.startsWith('image/')) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#filePreview').html('<img src="' + e.target.result + '" class="img-fluid" alt="Image Preview">');
            }
            reader.readAsDataURL(file);
        } else {
            $('#filePreview').html('<p>' + fileName + '</p>'); // Fallback for non-image files
        }
    });

    // Validate form before submission (ensure a file is selected)
    $('#uploadForm').submit(function(event) {
        if (!$('#fileInput').val()) {
            event.preventDefault();
            alert('Please select a file to upload.');
        }
    });

    // Loader functions
    function showLoader() {
        $("#loader-overlay").show();
    }

    function hideLoader() {
        $("#loader-overlay").hide();
    }

    // Show loader when the form is submitted
    $('#uploadForm').on('submit', function() {
        showLoader();
    });

    // Hide loader when window loads
    $(window).on('load', function() {
        hideLoader();
    });

    // Auto-hide alert messages
    function removeAlert() {
        setTimeout(function() {
            $(".alertBox").hide();
        }, 2000); // remove in 2 seconds
    }
});
