$(document).ready(function () {

    $('.ui.dropdown').dropdown();

    $('#show-account').click(function(){
        $('#account-modal')
            .modal('show')
        ;
    });

    $('#show-register').click(function(){
        $('#register-modal')
            .modal('show')
        ;
    });

    if (window.location.href.includes("next")) {
        $('#account-modal')
            .modal('show')
        ;
        $("#account-error-message").html("Please sign into your account to access this page!").show();
    }
});

