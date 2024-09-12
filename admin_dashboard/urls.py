from django.urls import path
from . import views

urlpatterns=[
    path("",views.admin_dashboard,name="admin_dashboard"),
    path("create_employee",views.create_employee,name="create_employee"),
    path("remove_employee",views.remove_employee,name="remove_employee"),
    path("create_store",views.create_store,name="create_store"),
    path("edit_store",views.edit_store,name="edit_store"),
    path("delete_store",views.delete_store,name="delete_store"),
    path("edit_profile",views.edit_profile,name="edit_profile"),
]