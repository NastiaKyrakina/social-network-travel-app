function PrevievFile() {
    // Отримання масиву
    var inputs = $('.file');

    label = {
        id_images: $('.file-list-image'),
        id_video: $('.file-list-video'),
        id_audio: $('.file-list-audio'),
        id_files: $('.file-list-file')
    }

    //Обробник події додання файлу
    inputs.change(function (e) {
        fileList = '';
        for (index in e.target.files) {
            if (this.files[index] instanceof File) fileList += '<p class="m-0 text-muted"><small>' +
                this.files[index].name + '</small></p>';
        }

        if (fileList) label[e.target.id].show();
        else label[e.target.id].hide();

        label[e.target.id].html(fileList);
    });
}


