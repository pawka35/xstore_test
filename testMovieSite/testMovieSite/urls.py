import sys

sys.path.append("..")
from django.contrib import admin
from django.urls import path, include

from moviesLibrary.views import router

urlpatterns = [
    path("", include("moviesLibrary.urls")),
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
]
