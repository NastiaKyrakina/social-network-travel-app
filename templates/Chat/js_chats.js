$('.chat-title').on('click', function (e) {
    e.preventDefault();
    $(".chat-container").load('/chat/chats/' + data.join + '/', function () {
        LoadMessages();
        RequaerUsers();
        $('.chat-title#block-' + data.join).closest('.new-message').removeClass("new-message");

        $(".message-form").load('/chat/create_message/',
            function () {

                PrevievFile();
                ShowDeleteMessage();
            });
    });
});