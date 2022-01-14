from django.conf.urls import url
from .views import FileUpload

urlpatterns = [
    url(r'^upload/$', FileUpload.as_view(), name='file-upload'),
]