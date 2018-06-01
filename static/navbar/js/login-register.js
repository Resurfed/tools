$(document).ready(function () {

    // semantic API stuff
    $.fn.api.settings.api = {
        'login': '/account/login/',
        'register': '/account/register/',
        'send-reset-email': '/account/send-reset-password/'
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

    $("#forget_password_redirect").click(function () {
        $("#forget-password-modal")
            .modal('show')
        ;
    });

    $('.message .close').on('click', function() { $(this).parent().hide(); });

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


    $('#send-reset-password-form')
        .form({
            keyboardShortcuts: false,
            fields: {
                reset_password_email: ['empty', 'email']
            }
        }).api({
        action: 'send-reset-email',
        method: 'POST',
        serializeForm: true,
        onSuccess: function (response) {
            // valid response and response.success = true
            $("#id_sent_email_message").show();
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