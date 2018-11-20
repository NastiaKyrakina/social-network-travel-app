$(document).ready(function () {
    $('.rate-stars').html(function () {
        var stars = '';
        for (var i = 1; i <= 5; i++) {
            if (i <= this.getAttribute('count')) stars += '<i class="fas fa-star"></i>';
            else stars += '<i class="far fa-star"></i>';
        }
        return stars;
    });
});