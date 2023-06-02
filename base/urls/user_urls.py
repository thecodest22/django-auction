from django.urls import path, include
from base.views import user_views as views


app_name = 'base_users'

urlpatterns = [
    path('', views.get_users, name="get_users"),
    path('<int:pk>/', include([
        path('', views.get_user_by_id, name="get_user"),
        path('update/', views.update_user, name="update_user"),  # PUT
        path('delete/', views.delete_user, name="delete_user"),  # DELETE
    ])),
    path('profile/', views.get_user_profile, name="user_profile"),
    path('profile/update/', views.update_user_profile, name="update_user_profile"),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
