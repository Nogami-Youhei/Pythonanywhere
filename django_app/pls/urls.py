from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('outline', views.outline, name='outline'),
    path('pls', views.pls, name='pls'),
    path('pcr', views.pcr, name='pcr'),
    path('scraping/', views.scraping, name='scraping'),
    path('upload', views.upload, name='upload'),
    
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.list, name='list'),
]