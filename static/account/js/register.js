$(document).ready(function () {

    $('.form')
        .form({
            keyboardShortcuts: true,
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
                password: {
                    identifier: 'password',
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
                            type: 'match[password]',
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

});