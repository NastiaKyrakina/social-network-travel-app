function GetIdCountry() {
    const inp = $("input#id_country").val();
    let opt = $("#countries option[value='" + inp + "']");
    return opt.attr('id');
}

function load_countrues(status = '1') {

    dataList = $("#countries");

    $.ajax({
        type: 'GET',
        async: true,
        url: '/load_countries/',
        data: "qc=" + status,
        success: function (data) {

            for (let i in data['dict']) {

                let option = document.createElement('option');
                option.value = data['dict'][i]['name'];
                option.id = data['dict'][i]['value'];
                if (status == '2') {
                    option.setAttribute('code', data['dict'][i]['phone_code']);

                }
                dataList.append(option);
            }

        },
        dataType: 'json',
    });
}