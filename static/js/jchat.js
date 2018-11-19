;

//Завантаження нової порції повідомлень
function LoadMessages() {
    $(".load_href_1").click(function () {

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

//Завантаження списку користувачів
function LoadUsers() {
    console.log('inp');
    dataList = $("#members_list");
    $('input#id_members').on('input', function () {
        $('.members-error').empty();
        q = $(this).val();
        $.ajax({
            type: 'GET',
            async: true,
            url: 'load/users/',
            data: "q=" + q,
            success: function (data) {
                dataList.empty();
                for (let i in data['users_list']) {
                    let option = document.createElement('option');
                    option.value = data['users_list'][i]['name'];
                    dataList.append(option);
                }

            }
        });
    });
}

//Перевірка на то, що користувача з даним ім'ям вже обрано
function UserAlreadyAdd(username) {
    let exs = false;
    $("#added-members li .username").each(function (index) {
        if (username == $(this).text()) {
            exs = true;
            return false;
        }
    });
    return exs;
}

//Додавання користвувача до списку
function AddUsers() {
    $("button#add-member").click(function (e) {
        e.preventDefault();

        let username = $("input#id_members").val();
        if (username && !UserAlreadyAdd(username)) {
            let member_list = $('#added-members');
            $.ajax(
                {
                    type: 'GET',
                    async: true,
                    url: 'get/user/',
                    data: "q=" + username,
                    success: function (data) {
                        console.log(data);
                        if (data != 'none') {
                            let list_el = document.createElement('li');
                            list_el.id = data['user_data'][1]['id'];

                            var del_link = "<span class='remove-el'> – </span>";
                            var username_block = "<span class='username'>" + data['user_data'][0]['name'] + "</span>";
                            list_el.innerHTML = username_block + del_link;
                            member_list.append(list_el);

                            RemoveMember();
                        }
                        else {
                            $('.members-error').text('user not found');
                        }
                    }

                });
        }
    });

}


function CreateConversation() {
    $("button#create-conversation").click(function (e) {
        e.preventDefault();
        $(".chat-container").load('create/convers/', function () {
            LoadUsers();
            $("#member-form").on('submit', function (e) {
                e.preventDefault();

                var form_memb = new FormData($(this).get(0));

                $.ajax(
                    {
                        type: $(this).attr('method'),
                        async: true,
                        contentType: false,
                        processData: false,
                        url: 'create/convers/',
                        data: form_memb,
                        success: function (data) {
                            if (data['status'] == 'success') {
                                console.log(data['slug']);
                                $(".chat-list").prepend(data['mini_chat']);
                                $(".chat-title#block-" + data['slug']).click();
                            }

                        }

                    });

                return false;
            });

        });

    });
}

//видалення користувача зі списку
function RemoveMember() {
    $(".remove-el").click(function (e) {
        $(this).closest("li").remove();
    });

}


function RequaerUsers() {
    console.log('rnp');

    $("button[id^=add-member-]").on('click', function () {
        slug = $(this).attr('id').split('-')[2];
        $(".add-member-block").load("add/members/" + slug, function () {
            console.log('inp');
            LoadUsers();
            AddUsers();

            $("#member-form").on('submit', function (e) {
                e.preventDefault();

                var members_list = [];

                $("#added-members li .username").each(function (index) {
                    members_list[index] = $(this).text();
                    console.log(members_list[index]);
                });

                $(this).get(0)['members'].value = members_list.join();
                console.log($(this).get(0)['members'].value);
                var form_memb = new FormData($(this).get(0));

                $.ajax(
                    {
                        type: $(this).attr('method'),
                        async: true,
                        contentType: false,
                        processData: false,
                        url: 'add/members/' + slug + "/",
                        data: form_memb,
                        success: function (data) {
                            if (data['status'] == 'success') {
                                console.log(data);
                                //$(".chat-list").prepend(data['mini_chat']);
                                //$(".chat-title#block-"+data['slug']).click();
                            }

                        }

                    });

                return false;
            });

            $('')

        });

    });
}

//створення чату
function CreateChat() {

    $("button#create-chat").click(function () {

        $(".chat-container").load('create/', function () {

            $(".chat-form").on('submit', function (e) {
                e.preventDefault();
                var form_chat = new FormData($(this).get(0));

                $.ajax(
                    {
                        type: $(this).attr('method'),
                        async: true,
                        contentType: false,
                        processData: false,
                        url: $(this).attr('action'),
                        data: form_chat,
                        success: function (data) {
                            if (data['status'] == 'success') {
                                console.log(data['slug']);
                                $(".chat-list").prepend(data['mini_chat']);
                                $(".chat-container").empty();
                                $(".chat-title#block-" + data['slug']).trigger('click');
                            }

                        }

                    });

                return false;
            });


        });

    });

    CreateConversation();
}

function ShowDelete() {

    $('.chat-title').hover(function () {

            $(this).find(".delete-button").removeAttr('hidden');
        },
        function () {

            $(this).find(".delete-button").attr('hidden', true);
        });
}