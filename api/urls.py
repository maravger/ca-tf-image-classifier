<<<<<<< HEAD
from django.conf.urls import *
from django.conf.urls import url
=======

from django.conf.urls import url

>>>>>>> refs/remotes/origin/master
from . import views

'''
urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^ocr/(?P<filename>[^/]+)$', views.ocr, name ='ocr'), 
            ]
'''
urlpatterns = [ 
<<<<<<< HEAD
        url(r'^imageUpload/(?P<filename>[^/]+)$', views.FileUploadView.as_view()),
        url(r'^getLogs/', views.metrics.GetLogs),
        url(r'^serverInfo/', views.postfromServer.post)
        ]
        

=======
        url(r'^imageUpload/(?P<filename>[^/]+)$', views.FileUploadView.as_view())
        ]
        
>>>>>>> refs/remotes/origin/master
