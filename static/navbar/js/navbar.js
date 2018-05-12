$(document).ready(function () {

    // semantic API stuff
    $.fn.api.settings.api = {
        'sign in': '/account/login/',
    };

    $.fn.api.settings.successTest = function (response) {
        console.log(response);
        if (response && response.success) {
            return response.success;
        }
        return false;
    };

    $('.ui.dropdown').dropdown();

    $('#login-button').on("click", function (e) {
        $('.ui.modal')
            .modal('show')
        ;
    });

    if (window.location.href.includes("next")) {
        $('.ui.modal')
            .modal('show')
        ;
        $(".ui.error.message").text("Please sign into your account to access this page!");
    }

    //Modal tabs
    $('.menu .item').tab();


    $('#signin-form')
        .form({
            keyboardShortcuts: false,
            fields: {
                user_name: {
                    identifier: 'user_name',
                    rules: [
                        {
                            type: 'empty',
                            prompt: 'Please enter your e-mail'
                        }
                    ]
                },
                password: {
                    identifier: 'password',
                    rules: [
                        {
                            type: 'empty',
                            prompt: 'Please enter your password'
                        },
                        {
                            type: 'length[6]',
                            prompt: 'Your password must be at least 6 characters'
                        }
                    ]
                }
            }
        }).api({
        action: 'sign in',
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

});

