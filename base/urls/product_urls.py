from django.urls import path, include
from base.views import product_views as views


app_name = 'base_products'

urlpatterns = [
    path('', views.get_products, name="get_products"),
    path('top/', views.get_top_products, name="top_products"),
    path('create/', views.create_product, name="create_product"),  # POST
    path('upload/', views.upload_image, name="upload_image"),  # POST
    path('<int:pk>/', include([
        path('', views.get_product, name="get_single_product"),
        path('reviews/', views.add_product_review, name="add_review"),  # POST
        path('update/', views.update_product, name="update_product"),  # PUT
        path('addprice/', views.increase_price, name="increase_price"),  # PUT
        path('delete/', views.delete_product, name="delete_product"),  # DELETE
    ])),
]
