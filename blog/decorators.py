from django.apps import apps 
from functools import wraps
import requests
import urllib
import json

def check_recaptcha(view_func):
    """
    This decorator checks a recaptcha before rending a view.
    Communicates with the view using the request object.
    Flash messages, if needed, are set in the view.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        recaptcha_enabled = apps.get_app_config('Blog').recaptcha_enabled
        secret_key = apps.get_app_config('Blog').recaptcha_secret
        request.recaptcha_is_valid = True
        if request.method == 'POST' and recaptcha_enabled:
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': secret_key,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
        return view_func(request, *args, **kwargs)
    return _wrapped_view