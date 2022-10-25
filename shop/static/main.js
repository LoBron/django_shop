$(function ($) {
    $('#login_form_ajax').submit(function (e) {
        e.preventDefault()
        console.log(this)
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            datatype: 'json',
            success: function (response) {
                console.log(response.status)
                if (response.status === 201) {
                    window.location.reload()
                } else if (response.status === 400) {
                    $('.alert-danger').text(response.error).removeClass('d-none')
                }

            }
//            error: function (response) {
//                console.log('-error', response)
//                if (response.status === 400) {
//                    $('.alert-danger').text(response.responseJSON.error).removeClass(value: 'd-none')
//                }
//            }
        })
    })

})