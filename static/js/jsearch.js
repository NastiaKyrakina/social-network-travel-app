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


    function set_valid_month(month) {
        console.log(sel_month);
        $("#id_public_month option").each(function (index) {

            if (index > month) {
                $(this).attr('hidden', 'hidden');
            }
            else {
                $(this).attr('hidden', false);
            }


        });
        console.log(sel_month);
    }

    function open_all_month() {
        $("#id_public_month option").attr('hidden', false);
    }

    function set_valid_day(day) {
        $("#id_public_day option").each(function (index) {
            if (index > (day - 1)) {
                $(this).attr('hidden', 'hidden');

            } else {
                $(this).attr('hidden', false);
            }
        });
    }

    $("#id_public_year").on('click',
        function () {

            get_year = $(this).val();
            if (get_year != sel_year) {

                sel_year = get_year;
                if (get_year == year) {

                    if (sel_month > (month + 1)) {
                        $("#id_public_month option:selected").attr('selected', false);
                        sel_month = (+month) + 1;

                        $("#id_public_month option[value=" + sel_month + "]").attr('selected', true);
                    }

                    set_valid_month(month);


                } else {
                    open_all_month();

                }
            }
        });

    $("#id_public_month").on('click',
        function () {
            get_month = $(this).val();
            console.log(sel_month);
            if (get_month != sel_month) {
                let temp_month;
                sel_month = get_month;
                if (sel_month == month) {
                    temp_month = day;
                } else {
                    temp_month = new Date(sel_year, sel_month, 0).getDate();
                }
                set_valid_day(temp_month);
            }

        });
}


$(document).ready(function () {

    SetSlider();
    load_countrues();
    CorrectDate();

    $('#form-multi-search').on('submit', function (e) {

        let urlParams = new URLSearchParams(window.location.search);
        $('#hide-text').attr('value', urlParams.get('text'));
        return;

    });

});
