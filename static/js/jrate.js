;

function RateSend(house_id) {
    $('#form-rate').on('submit', function (e) {
        //відміняємо стандартну відправку форми
        e.preventDefault();
        //отримання даних форми
        forms_1 = new FormData($(this).get(0));
        forms_1.append('house', house_id);

        //відправляємо дані
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            contentType: false,
            processData: false,
            data: forms_1,
            success: function (data) {

                if (typeof(data) === "object") {
                    alert(data['errors']);

                }
                else {
                    //додавання нового поста
                    $('.rate-block').prepend(data)
                    //очщення форми
                    $('#form-rate')[0].reset();

                }
            }


        });
        return false;
    });
}

function LoadRateForm() {
    var house_primary_key = $('[id^=house-element-]').attr('id').split('-')[2];
    $('#rate-add').load('/house/rate/', function () {
        //робота з додаванням постів тількі після завантаження блока
        RateSend(house_primary_key);
    });
    return false;
}


$(document).ready(function () {
    LoadRateForm();

});
