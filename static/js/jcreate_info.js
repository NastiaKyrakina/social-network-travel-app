$(document).ready(function () {

    load_countrues('2');

    $("input#id_country").on('change', function () {

        id_country = GetIdCountry();
        if (id_country === undefined && $(this).val().length > 0) {
            $(this).addClass('UncorrectValue');
        }
        else {
            $(this).removeClass('UncorrectValue');
            let code = $('option#' + id_country).attr('code');
            $('#phone-code').text(code);
        }

    });

    $('.info-form').submit(function (e) {

        id_country = GetIdCountry();
        if (id_country !== undefined) {
            $("input#id_country").val(id_country);
            code = $('#phone-code').text();
            $("input#id_phone_num").val(code + $("input#id_phone_num").val());
            return;
        }
        e.preventDefault();
        return false;
    });

});
