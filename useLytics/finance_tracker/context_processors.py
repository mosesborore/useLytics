from django.conf import settings


def check_debug_mode(request):
    context_extras = {}
    if settings.DEBUG:
        context_extras["debug_mode"] = True
    return context_extras
