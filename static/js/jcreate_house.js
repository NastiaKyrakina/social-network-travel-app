function GetIdCountry() {
    const inp = $("input#id_country").val();
    let opt = $("#countries option[value='" + inp + "']");
    return opt.attr('id');
}

$(document).ready(function () {

    var CountryCorrect;
    load_countrues();

    $("input#id_country").on('change', function () {

        id_country = GetIdCountry();
        if (id_country === undefined && $(this).val().length > 0) {
            $(this).addClass('UncorrectValue');
        }
        else {
            $(this).removeClass('UncorrectValue');
        }

    });

    $('.house-form').submit(function (e) {

        id_country = GetIdCountry();
        if (id_country !== undefined) {
            $("input#id_country").val(id_country);
            return;
        }
        e.preventDefault();
        return false;
    });

});
