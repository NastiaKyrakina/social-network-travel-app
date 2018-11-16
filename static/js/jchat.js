;
const TALK = 0;
const PRIVATE = 1;
const PUBLIC = 1;

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

function LoadUsers() {
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

function UserAlreadyAdd(username) {
    let exs = false;
    $("#added-members li .username").each(function (index) {

        console.log($(this).text());
        if (username == $(this).text()) {
            exs = true;
            return false;
        }

    });
    return exs;
}

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
                            console.log(data['user_data'][0]['name']);
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

function RemoveMember() {
    $(".remove-el").click(function (e) {
        $(this).closest("li").remove();
    });

}

function GetSelectType() {
    return $(".chat-type-select input[name=chat_type]:checked").val()
}

function CreateChat() {
    $("button#create-chat").click(function () {

        $(".chat-container").load('create/', function () {
            LoadUsers();

            AddUsers();


        });

    });


}