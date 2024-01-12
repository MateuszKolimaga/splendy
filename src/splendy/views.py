from django.http import HttpResponseRedirect
from django.conf import settings


def redirect_to_login(request):
    if request.GET.get("verification") == "1":
        return HttpResponseRedirect(settings.FRONTEND_URL + "/login?verification=1")
    elif request.GET.get("invitation"):
        return HttpResponseRedirect(settings.FRONTEND_URL + "/?invitation={invitation}")
    else:
        return HttpResponseRedirect(settings.FRONTEND_URL)
