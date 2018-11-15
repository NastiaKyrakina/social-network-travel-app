function LoadMessages() {
    $(".load_href_1").click(function () {
        console.log('cls');
        var chat_slug = $('.Chat').attr('id');
        var qr = $(".content>:first-child .message-date small").text();

        $.ajax({
            type: 'GET',
            async: true,
            url: 'chats/' + chat_slug + '/',
            data: "since=" + qr,
            success: function (data) {
                $(".content").prepend(data)
            },

        });

    });
}