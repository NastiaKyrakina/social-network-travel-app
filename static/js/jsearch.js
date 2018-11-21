function SetSlider() {

    var min_v = Number($("#id_min_price").attr('min'));
    var max_v = Number($("#id_max_price").attr('max'));
    $("#slider_min_max_price").slider({
        range: true,
        min: min_v,
        max: max_v,
        step: 1.00,
        values: [min_v, max_v],

        slide: function (event, ui) {
            $("#id_min_price").val(ui.values[0] + '.00');
            $("#id_max_price").val(ui.values[1] + '.00');
        }
    });

    $("#id_min_price").change(function () {
        var val = $(this).val();
        $("#slider_min_max_price").slider("values", 0, val);
    });

    $("#id_max_price").change(function () {
        var val = $(this).val();
        $("#slider_min_max_price").slider("values", 1, val);
    });
    return false;

}

function CorrectDate() {
    let now = new Date();
    let year = now.getFullYear();
    let month = now.getMonth();
    let day = now.getDate();

    $("#id_public_year option[value='']").remove();
    $("#id_public_month option[value='']").remove();
    $("#id_public_day option[value='']").remove();

    let sel_year = $("#id_public_year option:selected").val();
    let sel_month = $("#id_public_month option:selected").val();
    let sel_day = $("#id_public_day option:selected").val();


    $("#id_public_month option[value=10]");

    function set_valid_month(month) {
        $("#id_public_month option").each(function (index) {
            if (index > month) {
                $(this).attr('hidden', 'hidden');
            }
            else {
                $(this).attr('hidden', false);
            }
        });
    }

    function open_all_month() {
        $("#id_public_month option").attr('hidden', false);
    }

    function open_all_day() {
        $("#id_public_day option").attr('hidden', false);
    }

    function set_valid_day(day) {
        $("#id_public_day option").each(function (index) {
            if (index > (day)) {
                $(this).attr('hidden', 'hidden');
                console.log($(this).val());
                console.log(day);
            }
        });
    }


    $("#id_public_year").on('click',
        function () {
            get_year = $(this).val();
            console.log(get_year);
            console.log(year);
            console.log(month);
            if (get_year != sel_year) {
                sel_year = get_year;
                if (get_year == year) {
                    console.log('set');
                    set_valid_month(month);
                    if (sel_month > month) {
                        sel_month = month;
                        $("#id_public_month option[value=" + sel_month + "]").attr('selected', 'selected');
                    }
                } else {
                    open_all_month();
                }
            }
        });

    $("#id_public_month").on('change',
        function () {
            get_month = $(this).val();
            if (get_month != sel_month) {
                sel_month = get_month;
                if (sel_month == month) {
                    set_valid_day(day);
                }
                else {
                    max_day = new Date(sel_year, sel_month, 0);
                    set_valid_day(max_day);
                }
            }

        });
}


$(document).ready(function () {

    SetSlider();
    load_countrues();
    CorrectDate();

    $('#form-multi-search').on('submit', function (e) {
        console.log('submit');
        let urlParams = new URLSearchParams(window.location.search);
        $('#hide-text').attr('value', urlParams.get('text'));
        return;

    });

});
