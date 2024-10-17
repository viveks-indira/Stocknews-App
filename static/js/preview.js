// Preview the image before uploading
function previewImage(event) {
    var reader = new FileReader();
    var imageField = document.getElementById("preview");

    reader.onload = function() {
        if (reader.readyState == 2) {
            imageField.src = reader.result;
            imageField.style.display = 'block';  // Show the image preview
        }
    };

    reader.readAsDataURL(event.target.files[0]);
}
