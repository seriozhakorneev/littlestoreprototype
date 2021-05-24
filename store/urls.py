from django.urls import path

from . import views

app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:product_id>/', views.detail, name='detail'),
    path('basket/', views.basket, name='basket'),
    path('add/<int:product_id>/', views.add_product_to_s_basket, name='add_product_to_s_basket'),
    path('del/<int:product_id>/', views.delete_product_from_s_basket, name='delete_product_from_s_basket'),
    path('clear/', views.clear_s_basket, name='clear_s_basket'),
]