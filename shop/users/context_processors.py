from .forms import AuthenticationAjaxForm


def get_login_form(request):
    return {'login_ajax': AuthenticationAjaxForm()}
