function GetIdCountry() {

    const inp = $("input#id_country").val();
    let opt = $("#countries option[value='" + inp + "']");
    return opt.attr('id');
}

function TrimInput() {

    $('input[type=text]').on('input', function () {
        var text = $(this).val();
        text = text.replace(/^\s*/g, "")
        $(this).val(text.replace(/\s+/g, " "));

    });
}

function CorrectRegistr() {

    $('input[type=text]').on('input', function (e) {

        var text = $(this).val();
        var text_list = text.toLowerCase().split(/[\s`ʼ-]+/);
        for (let i = 0; i < text_list.length; i++) {
            text_list[i] = text_list[i].charAt(0).toUpperCase() + text_list[i].slice(1);
        }

        let k = 1;
        var new_text = text_list[0];
        for (let i = 0; i < text.length && k < text_list.length; i++) {
            let char = text.charAt(i);
            if (char.search(/[\s`ʼ-]+/) > -1) {
                new_text += char + text_list[k];
                k = k + 1;
            }

        }
        $(this).val(new_text);
    });
}

function DelUncorrectSimvol() {

    $('input[name=city],input[name=title]').on('keydown', function (e) {

        key = e.key;
        // спец. сочетание - не обрабатываем
        if (e.ctrlKey || e.altKey || e.metaKey) return;

        key = e.key;
        if (!key) return;
        if (key.search(/[\w\sA-Za-zА-Яа-яіІєЄйЙїЇ`ʼ-]+/) === -1) return false;

    });
}

function OnlyLatOrKir() {

    $('input[name=city]').on('change', function (e) {

        var lat;
        var kir;
        text = $(this).val();
        lat = text.search(/[\w]+/);
        kir = text.search(/[А-Яа-яіІєЄйЙїЇ]+/);

        if (lat !== -1 && kir !== -1) {

        }

    });
}


$(document).ready(function () {

    DelUncorrectSimvol();
    TrimInput();
    CorrectRegistr();
    OnlyLatOrKir();

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
