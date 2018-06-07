$(document).ready(function () {

    $.fn.api.settings.api = {
        'login': '/account/login/',
        'register': '/account/register/',
        'forget-password': '/account/forget/',
        'reset-password': '/account/reset/'
    };

    $.fn.api.settings.successTest = function (response) {
        console.log(response);
        if (response && response.success) {
            return response.success;
        }
        return false;
    };

    $.fn.form.settings.rules.spawns = function (value) {

        if (value.length === 0)
            return true;

        let pattern = /^(map::-?\d+,-?\d+,-?\d+:-?\d+,-?\d+,-?\d+|(stage|bonus):([1-9]\d*):-?\d+,-?\d+,-?\d+:-?\d+,-?\d+,-?\d+)$/;
        let lines = value.split("\n");
        let ret_value = true;

        $.each(lines, function (i) {
            if (!pattern.test(lines[i])) {
                ret_value = false;
                return false;
            }
        });

        return ret_value;
    };

});