$(document).ready(function () {

    $(".house").on('click', 'button[id^=edit-element-]',
        function () {
            var house_primary_key = $(this).attr('id').split('-')[2];
            location.href = '/house/edit/' + house_primary_key + '/'

        });

    $(".house").on('click', 'button[id^=delete-element-]',
        function () {
            var house_primary_key = $(this).attr('id').split('-')[2];
            delete_house(house_primary_key)

        });

    function delete_house(house_primary_key) {
        if (confirm('are you sure you want to remove this post?') == true) {

            $.ajax({
                url: "/house/delete/", // the endpoint
                type: "POST", // http method
                data: {
                    csrfmiddlewaretoken: Cookies.get('csrftoken'),
                    housepk: house_primary_key
                }, // data sent with the delete request
                success: function (json) {

                    location.href = '/user/1/'

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


    function contact_with_owner() {

        $.ajax({
            url: "/chat/start-conver/", // the endpoint
            type: "POST", // http method
            data: {
                csrfmiddlewaretoken: Cookies.get('csrftoken'),
                housepk: house_primary_key
            }, // data sent with the delete request
            success: function (json) {

                location.href = '/user/1/'

            },

            error: function (xhr, errmsg, err) {
                // Show an error
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }

else
    {
        return false;
    }

});

