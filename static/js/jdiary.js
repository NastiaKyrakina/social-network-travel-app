$(document).ready(function () {


    $(".diary").on('click', 'button[id^=edit-element-]',
        function () {
            var diary_primary_key = $(this).attr('id').split('-')[2];
            loc = location.pathname.split('/')[1];
            location.href = '/' + loc + '/user/diary/edit/' + diary_primary_key + '/';

        });

    $(".diary").on('click', 'button[id^=delete-element-]',
        function () {
            var diary_primary_key = $(this).attr('id').split('-')[2];
            let action = $(this).attr('formaction');
            delete_diary(diary_primary_key, action);

        });

    $(".diary").on('click', 'button[id^=change-element-]',
        function () {
            var diary_primary_key = $(this).attr('id').split('-')[2];
            let action = $(this).attr('formaction');
            change_status(diary_primary_key, action);

        });

    function delete_diary(diary_primary_key, action) {
        if (confirm('are you sure you want to remove this diary?') == true) {

            $.ajax({
                url: action, // the endpoint
                type: "POST", // http method
                data: {
                    csrfmiddlewaretoken: Cookies.get('csrftoken'),
                    diarypk: diary_primary_key
                }, // data sent with the delete request
                success: function (json) {

                    location.href = '/user/' + json.locate;

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


    function change_status(diary_primary_key, action) {

        $.ajax({
            url: action, // the endpoint
            type: "POST", // http method
            data: {
                csrfmiddlewaretoken: Cookies.get('csrftoken'),
                diarypk: diary_primary_key
            }, // data sent with the delete request
            success: function (status) {

                if (status.status == 'fail') {
                    alert('Status was not be change');
                } else {
                    let status_span;
                    let button = $('.button-status');

                    if (status.status) {
                        button.text('active');
                        $('.diary-status .text-success').attr('hidden', true);
                        $('.diary-status .text-info').attr('hidden', false);


                    } else {

                        button.text('frozen');
                        $('.diary-status .text-success').attr('hidden', false);
                        $('.diary-status .text-info').attr('hidden', true);

                    }

                }
            },

            error: function (xhr, errmsg, err) {
                // Show an error
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });

    }

});

