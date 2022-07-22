from django.urls import path
from . import views

urlpatterns = [
    # 登陆
    path('', views.login),
    path('log_in/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    # 管理员
    path('admin/', views.admin),
    path('admin/<int:nid>/edit/', views.admin_edit),
    path('admin/delete/', views.admin_delete),
    # 用户
    path('customer/detection/', views.customer_detection),
    path('customer/detection/draw/', views.draw1),
    path('customer/info/', views.customer_info),
    path('customer/info2/', views.customer_info_2),
    path('customer/info/delete/', views.customer_info_delete)
]
