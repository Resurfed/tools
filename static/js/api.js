$(document).ready(function () {

    $.fn.api.settings.api = {
        'login': '/account/login/',
        'register': '/account/register/',
        'forget-password': '/account/forget/'
    };

    $.fn.api.settings.successTest = function (response) {
        console.log(response);
        if (response && response.success) {
            return response.success;
        }
        return false;
    };

});