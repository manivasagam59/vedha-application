from django.urls import path
from . import views

urlpatterns=[
    path("",views.store_dashboard,name="store_dashboard"),
    path("mobile_recharge",views.mobile_recharge,name="mobile_recharge"),
    path("dth_recharge",views.dth_recharge,name="dth_recharge"),
    path("online_services",views.online_services,name="online_services"),
    path("product_sales",views.product_sales,name="product_sales"),
    path("product_sales/bill/<str:id>",views.bill_view,name="bill_view"),
    path("edit",views.edit_profile,name="emp_edit_profile"),
    path("accounting",views.accounting,name="accounting"),
    path("stock_management",views.stock_management,name="stock_management")
]