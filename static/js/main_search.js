function MainSearch() {
    let urlParams = new URLSearchParams(window.location.search);

    $('#search-text').attr('value', urlParams.get('text'))


}


$(document).ready(function () {

    MainSearch();

});