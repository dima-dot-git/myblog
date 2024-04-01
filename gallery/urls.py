from django.urls import path
from .views import gallery, upload

urlpatterns = [

    path("", gallery, name='gallery'),
    path("uploads/", upload, name="upload")
]
