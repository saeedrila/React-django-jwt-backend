from django.urls import path,include
from . import views

urlpatterns = [
    path('register/',views.CustomUserCreate.as_view(),name="create_user"),
    path('login/',views.UserLoginView.as_view(),name="login"),
    path('admin/',views.AdminLoginView.as_view(),name="admin"),
    path('logout/',views.LogoutView.as_view(),name="logout"),
    path('userlist/',views.UserListAPIView.as_view(),name='userlist'),
    path('edit_user/<int:pk>',views.UserEditAPIView.as_view(),name="edit_user"),
    path('edit_user/',views.UserEditAPIView.as_view(),name="edit_users"),
    path('search_user/',views.UserSearchApiView.as_view(),name="search_user"),
    path('user_profile/<int:pk>',views.UserProfileView.as_view(),name="user_profile"),
    path('check_auth/',views.CheckAuthView.as_view(),name="check_auth"),
]
