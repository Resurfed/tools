$(document).ready(function () {
    $('.form')
        .form({
            keyboardShortcuts: true,
            fields: {
                user_name: 'empty',
                email: ['empty', 'email']
            }
        }).api({
        action: 'forget-password',
        method: 'POST',
        serializeForm: true,
        onSuccess: function (response) {
            // valid response and response.success = true
            $(".ui.positive.message").show();
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