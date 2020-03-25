from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name='dict-home'),
    path('about/', views.about, name='dict-about'),
    url(r'^$', views.button),
    url(r'^output', views.output,name="script"),
    path('about/', views.home),
    url(r'^testing/$', views.return_data),
    path('pose_view/', views.pose_create_view)
]