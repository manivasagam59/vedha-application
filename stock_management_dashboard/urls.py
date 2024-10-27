from django.urls import path
from . import views

urlpatterns=[
    path("",views.stock_management,name="stock_management"),
    path("/stocks",views.stocks,name="stocks"),
    path("/supplier",views.supplier,name="supplier"),
    path("/buying_history",views.buying_history,name="buying_history"),
    path("/edit",views.edit_profile,name="stock_manager_emp_edit")
]