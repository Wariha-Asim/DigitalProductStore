from . import views
from django.urls import path

urlpatterns = [
    path('login/',views.login, name='login'),
    path('signup/',views.signup, name='signup'),
    path('showall/',views.showall, name='showall'),
    path('delete/<int:id>/',views.deleteprod, name='deleteprod'),
    path('deleteall/',views.deleteall, name='deleteall'),
    path('addprod/',views.createprod, name='createprod'),
    path('logout/', views.logout, name='logout'),
    path('update-product/<int:product_id>/', views.update_product, name='updateprod'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('password_reset/', views.password_reset_email, name='password_reset_email'),
    path('password_reset/code/', views.password_reset_code, name='password_reset_code'),
    path('password_reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
]