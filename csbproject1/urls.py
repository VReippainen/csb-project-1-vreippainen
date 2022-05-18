from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("recipe/", include("recipe.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
]
