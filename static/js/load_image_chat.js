function handleFileSelect(evt) {
    var file = evt.target.files; // FileList object
    var f = file[0];
    // Only process image files.
    if (!f.type.match('image.*')) {
        alert("Image only please....");
    }
    var reader = new FileReader();
    // Closure to capture the file information.
    reader.onload = (function (theFile) {
        return function (e) {
            // Render thumbnail.
            var r = document.getElementById('output');
            r.InherritHTML = '';

            r.innerHTML = ['<img class="img-fluid" title="', escape(theFile.name), '" src="', e.target.result, '" />'].join('');


        };
    })(f);
    // Read in the image file as a data URL.
    reader.readAsDataURL(f);
}

document.getElementById('id_image').addEventListener('change', handleFileSelect, false);
document.getElementById('id_image').addEventListener('load', handleFileSelect, false);
