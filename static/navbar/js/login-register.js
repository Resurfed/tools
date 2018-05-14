$(document).ready(function () {

    // semantic API stuff
    $.fn.api.settings.api = {
        'login': '/account/login/',
        'register': '/account/register/'

    };

    $.fn.api.settings.successTest = function (response) {
        console.log(response);
        if (response && response.success) {
            return response.success;
        }
        return false;
    };

    $('#register_redirect').click(function () {
        $('#register-modal')
            .modal('show')
        ;
    });

    $('#login_redirect').click(function () {
        $('#login-modal')
            .modal('show')
        ;
    });

    $('#signin-form')
        .form({
            keyboardShortcuts: false,
            fields: {
                user_name: 'empty',
                password: ['empty', 'minLength[6]', 'maxLength[32]']
            }
        }).api({
        action: 'login',
        method: 'POST',
        serializeForm: true,
        onSuccess: function (response) {
            // valid response and response.success = true
            window.location.replace(response.redirect);
        },
        onFailure: function (response) {
            $(".ui.error.message").text(response.errors);
        }
    });

    $('#register-form')
        .form({
            keyboardShortcuts: false,
            fields: {
                user_name: {
                    identifier: 'user_name',
                    rules: [
                        {
                            type: 'empty'
                        }
                    ]
                },
                email: {
                    identifier: 'email',
                    rules: [
                        {
                            type: 'email'
                        },
                        {
                            type: 'empty'
                        }
                    ]

                },
                register_password: {
                    identifier: 'register_password',
                    rules: [
                        {
                            type: 'empty'
                        }, {
                            type: 'minLength[6]'
                        }, {
                            type: 'maxLength[32]'
                        }
                    ]
                },
                confirm_password: {
                    identifier: 'confirm_password',
                    rules: [
                        {
                            type: 'empty'
                        },
                        {
                            type: 'match[register_password]',
                            prompt: 'Passwords do not match!'
                        }
                    ]
                }
            }
        }).api({
        action: 'register',
        method: 'POST',
        serializeForm: true,
        onSuccess: function (response) {
            // valid response and response.success = true
            window.location.replace(response.redirect);
        },
        onFailure: function (response) {

            let errors = response.errors[0];

            let list = '<ul class="list">';
            for (let key in errors) {
                if (errors.hasOwnProperty(key)) {
                    for (let x = 0; x < errors[key].length; x++) {
                        list += '<li>' + errors[key][x] + '</li>'
                    }
                }
            }
            list += '</ul>';


            $(".ui.error.message").html(list);
        }
    });
});