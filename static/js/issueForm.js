$(function() {
    $("#id_issue_status").change(function() {
        if ($(this).val() == 'feature') {
            $('.payment-message').show();
            $('.payment-form').show();
        }
        else {
            $('.payment-message').hide();
            $('.payment-form').hide();
        }
    });
});
