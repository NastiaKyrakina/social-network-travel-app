function GetIdCountry() {

    const inp = $("input#id_country").val();
    let opt = $("#countries option[value='" + inp + "']");
    return opt.attr('id');
}

function TrimInput() {

    $('input[type=text]').on('input', function () {
        var text = $(this).val();
        text = text.replace(/^\s*/g, "");
        $(this).val(text.replace(/\s+/g, " "));

    });
}

function TextAreaTrim() {
    $('textarea').on('input', function () {
        var text = $(this).val();
        text = text.replace(/^ */g, "");
        $(this).val(text.replace(/ +/g, " "));

    });
}

function TextAreaCountChar() {
    $('textarea').on('input', function () {
        var count = $(this).val().length;
        if (count <= 100) {
            $(".sucs-show").hide();
            $(".character-counter").show();
            $('#counter').text(100 - count);
        } else {
            $(".character-counter").hide();
            $(".sucs-show").show();
        }

    });
}


function FirstSimvolToUpper(input_selector) {
    $(input_selector).on('input', function (e) {
        var text = $(this).val();
        $(this).val(text.charAt(0).toUpperCase() + text.slice(1));
    });
}

function CorrectRegistr(input_selector) {

    $(input_selector).on('input', function (e) {

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

function DelUncorrectSimvol(input_selector, other_simvol = '') {

    $(input_selector).on('keydown', function (e) {

        key = e.key;
        // спец. сочетание - не обрабатываем
        if (e.ctrlKey || e.altKey || e.metaKey) return;

        key = e.key;
        if (!key) return;
        reg = new RegExp('[\\sA-Za-zА-Яа-яіІєЄйЙїЇЁё`ʼ' + other_simvol + '-]+');
        if (key.search(reg) === -1) return false;

    });
}

function OnlyLatOrKir(input_selector) {

    let correct = true;
    $(input_selector).on('change', function (e) {

        var lat;
        var kir;
        text = $(this).val();
        lat = text.search(/[A-Za-z]+/);
        kir = text.search(/[А-Яа-яіІєЄйЙїЇ]+/);

        if (lat !== -1 && kir !== -1) {
            correct = false;
        }

    });

    return correct;
}

function AddressValidation() {
    $("input[name=address]").on('change', function (e) {
        text = $(this).val();
        text_arr = text.split(',');
        if (text_arr.length > 3) {
            error = "Uncr";
            console.log('err');
        } else {

            if (text_arr[0].length == 0) {
                console.log('err0');
            } else {
                text_arr[0].trim();
                reg = new RegExp('^[0-9A-Za-zА-Яа-яЇїІієЄЁё]+[\0-9A-Za-zА-Яа-яЇїІієЄЁё`ʼ-]*$');
                console.log(text_arr[0].search(/[A-Za-zА-Яа-яіІєЄйЙїЇ]/));
                if (reg.test(text_arr[0]) && text_arr[0].search(/[A-Za-zА-Яа-яіІєЄйЙїЇ]/) > -1) {
                    console.log('val1');
                }

            }
            if (text_arr[1].length == 0) {
                console.log('err1');
            } else {
                text_arr[1].trim();
                reg = new RegExp('[0-9]{1,4}-*[0-9A-Za-zА-Яа-яЇїІієЄЁё]');
                console.log('ww');
                if (reg.test(text_arr[1])) {
                    console.log('val2');
                }
            }
            if (text_arr[2] && text_arr[2].length == 0) {
                console.log('del2');
            }


        }


    });
}


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
        if (id_country !== undefined) {
            $("input#id_country").val(id_country);
            return;
        }
        e.preventDefault();
        return false;
    });


});
