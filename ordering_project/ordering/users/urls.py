from django.urls import path

from .views import (
    users_list_view,
    register_view,
    login_view,
    logout_view,
    user_detail_view,
    user_detail_delete_view
)


app_name = 'users'

urlpatterns = [
    path(
        route='',
        view=users_list_view,
        name='list'
    ),
    path(
        route='profile/<int:pk>/',
        view=user_detail_view,
        name='profile'
    ),
    path(
        route='profile/<int:pk>/delete',
        view=user_detail_delete_view,
        name='profile_delete'
    ),

    path(
        route='register/',
        view=register_view,
        name='register'
    ),
    path(
        route='login/',
        view=login_view,
        name='login'
    ),
    path(
        route='logout/',
        view=logout_view,
        name='logout'
    )
]
