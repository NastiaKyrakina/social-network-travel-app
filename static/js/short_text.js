$(".note-text").each(function () {
    var review_full = jQuery(this).html();
    var review = review_full;

    if (review.length > 500) {
        review = review.substring(0, 500);
        jQuery(this).html(review + '...<div class="read-more">more&rarr;</div>');

    }
    jQuery(this).append('<div class="full-text" style="display: none;">' + review_full + '</div>');
});

$(".note-text .read-more").click(function () {
    jQuery(this).parent().html(jQuery(this).parent().find(".full-text").html());
});