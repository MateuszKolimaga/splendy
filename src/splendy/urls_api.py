from django.contrib import admin
from django.urls import include, path, re_path
from allauth.account.views import confirm_email
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("teams/", include("teams.urls")),
    path("personal/", include("personal.urls")),
    ####AUTH
    re_path(r"^auth/", include("dj_rest_auth.urls")),
    re_path(r"^registration/", include("dj_rest_auth.registration.urls")),
    re_path(r"^account/", include("allauth.urls")),
    re_path(
        r"^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$",
        confirm_email,
        name="account_confirm_email",
    ),
    ####SWAGGER
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
