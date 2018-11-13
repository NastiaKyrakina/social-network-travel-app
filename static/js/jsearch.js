function SetSlider() {

    $("#slider_min_max_price").slider({
        range: true,
        min: 0.00,
        max: 999.99,
        step: 1.00,
        values: [0.00, 999.00],

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


$(document).ready(function () {

    //SetSlider();
    load_countrues();

    $('#form-multi-search').on('submit', function (e) {

        let urlParams = new URLSearchParams(window.location.search);
        $('#hide-text').attr('value', urlParams.get('text'));
        return;

    });

});
