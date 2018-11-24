

$(document).ready(function () {


    $(".sucs-show").hide();

    DelUncorrectSimvol('input[name=city],input[name=country]');
    DelUncorrectSimvol('input[name=address]', '0-9,');
    TrimInput();
    TextAreaTrim();
    TextAreaCountChar();
    CorrectRegistr('input[name=city],input[name=country],input[name=address]');
    OnlyLatOrKir('input[name=city]');
    FirstSimvolToUpper('input[name=title]');

    AddressValidation();
    AddresTitle();

    load_countrues();

    $("input#id_country").on('change', function () {

        var id_country = GetIdCountry();
        if (id_country === undefined && $(this).val().length > 0) {
            $(this).addClass('UncorrectValue');
            $(".js-country-error").removeAttr('hidden');
        } else {
            $(this).removeClass('UncorrectValue');
            $(".js-country-error").attr('hidden', true);
        }

    });

    $('.house-form').submit(function (e) {


        id_country = GetIdCountry();
        if (id_country === undefined) {

            e.preventDefault();
            return false;
        } else {

            if ($(this).find('#id_about').val().length < 100) {
                $(this).find('.js-about-error').attr('hidden', false);
                return false;
            } else if (!OnlyLatOrKir) {
                return false;
            }
        }
        $("input#id_country").val(id_country);
        return;


    });


});
