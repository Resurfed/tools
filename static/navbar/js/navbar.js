$(document).ready(function () {

    $('.ui.dropdown').dropdown();

    $('#show-login').click(function(){
        $('#login-modal')
            .modal('show')
        ;
    });

    $('#show-register').click(function(){
        $('#register-modal')
            .modal('show')
        ;
    });

    if (window.location.href.includes("next")) {
        $('.ui.modal')
            .modal('show')
        ;
        $(".ui.error.message").text("Please sign into your account to access this page!");
    }

});

