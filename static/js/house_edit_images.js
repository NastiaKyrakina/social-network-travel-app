$(document).ready(function () {
    $('#id_image').change(function (e) {
        var images = e.target.files;
        $('#house-images-board img').remove();
        for (index in images) {
            if (images[index] instanceof File) {
                var reader = new FileReader();
                reader.onload = (function (theFile) {
                    return function (e) {
                        $('<img src="' + e.target.result + '" class="house-image img-fluid m-1">').appendTo('#house-images-board');
                    };
                })(images[index]);
                // Read in the image file as a data URL.
                reader.readAsDataURL(images[index]);
            }
        }

    });
});