function LoadFile() {

    var inputs = $('.file');

    label = {
        id_images: $('.file-list-image'),
        id_video: $('.file-list-video'),
        id_audio: $('.file-list-audio'),
        id_files: $('.file-list-file')
    };

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

    //якщо форму відправлено
    $('.form-post-add').on('submit', function (e) {
        //відміняємо стандартну відправку форми
        e.preventDefault();
        //отримання даних форми
        forms_1 = new FormData($(this).get(0));
        //відправляємо дані
        console.log($(this).attr('method'));
        console.log(forms_1);
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            contentType: false,
            processData: false,
            data: forms_1,
            success: function (data) {

                if (typeof(data) === "object") {
                    console.log('err');
                    alert(data['errors']);

                }
                else {
                    console.log('data');
                    //додавання нового поста
                    $('.user-posts').prepend(data)
                    //очщення форми
                    $('.form-post-add')[0].reset();
                    $('.file-label').empty();
                }
            }

        });
        return false;
    });


}

function LoadPostCreateForm() {
    $('.create-node').load('/user/note/create/', function () {
        //робота з додаванням постів тількі після завантаження блока

        LoadFile();
    });
    return false;
}

$(document).ready(function () {

    LoadPostCreateForm();


    $(".note").on('click', 'button[id^=edit-element-]',
        function () {
            var post_primary_key = $(this).attr('id').split('-')[2];
            $('#note_element-' + post_primary_key + ' .note-text').load('/user/note/edit/' + post_primary_key,
                function () {
                    $('#note_element-' + post_primary_key + ' .note-form').attr('id', 'edit-' + post_primary_key);
                }
            );

        });

    $(document).on('submit', '.note-form',
        function SendFormAjax() {
            var post_primary_key = $(this).attr('id').split('-')[1];
            $.ajax({
                type: $(this).attr('method'),
                url: '/user/note/edit/' + post_primary_key + '/',
                data: $(this).serialize(),
                context: this,
                success: function (data) {
                    if (data['status'] !== 'success') {
                        alert('The note didn`t save');
                    }
                    $('#note_element-' + post_primary_key + ' .note-text').html(data['text'].toString());
                }
            });
            return false;
        });


    $(".note").on('click', 'button[id^=delete-element-]',
        function () {
            var post_primary_key = $(this).attr('id').split('-')[2];
            delete_post(post_primary_key);
        });

    function delete_post(post_primary_key) {
        if (confirm('are you sure you want to remove this post?') == true) {

            $.ajax({
                url: "/user/note/delete/", // the endpoint
                type: "POST", // http method
                data: {
                    csrfmiddlewaretoken: Cookies.get('csrftoken'),
                    notepk: post_primary_key
                }, // data sent with the delete request
                success: function (json) {
                    // hide the post
                    $('#note_element-' + post_primary_key).hide(); // hide the post on success
                    console.log(json['msg'].toString());

                },

                error: function (xhr, errmsg, err) {
                    // Show an error
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });
        } else {
            return false;
        }
    }


    $(".load_href_1").click(function () {

        var qr = $(".user-posts >:last-child .note_date small").text();

        $.ajax({
            type: 'GET',
            async: true,
            url: 'load_notes/',
            data: "since=" + qr,
            success: function (data) {
                $(".user-posts").append(data['html'])
            },
            dataType: 'json',
        });

    });


});

