$(document).ready(function () {
    $('.form')
        .form({
            keyboardShortcuts: true,
            fields: {
                user_name: 'empty',
                password: ['empty', 'minLength[6]', 'maxLength[32]']
            },
        }).api({
        action: 'login',
        method: 'POST',
        serializeForm: true,
        onSuccess: function (response) {
            // valid response and response.success = true
            window.location.replace(response.redirect);
        },
        onFailure: function (response) {

            let errors = response.errors;

            let list = '<ul class="list">';
            for (let key in errors) {
                if (errors.hasOwnProperty(key)) {
                    list += '<li>' + errors[key] + '</li>'
                }
            }
            list += '</ul>';

            $(".ui.error.message").html(list);
        }
    });
});