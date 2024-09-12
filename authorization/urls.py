from django.urls import path
from . import views

urlpatterns=[
    path("",views.home,name="home"),
    path("login/",views.login,name="store_login"),
    path("admin_login/",views.admin_login,name="admin_login"),
    path("logout/",views.logout,name="logout"),
]