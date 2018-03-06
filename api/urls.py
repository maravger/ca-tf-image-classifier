
from django.conf.urls import url

from . import views

'''
urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^ocr/(?P<filename>[^/]+)$', views.ocr, name ='ocr'), 
            ]
'''
urlpatterns = [ 
        url(r'^imageUpload/(?P<filename>[^/]+)$', views.FileUploadView.as_view())
        ]
        
