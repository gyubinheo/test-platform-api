from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include("problems.urls")),
    path("submissions/", include("submissions.urls")),
    # path("accounts/", include("accounts.urls")),
]
