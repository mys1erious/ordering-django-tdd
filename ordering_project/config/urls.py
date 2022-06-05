from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from core.views import main_page


urlpatterns = [

    # Apps
    path(
        route='',
        view=main_page,
        name='home_page'
    ),
    path(
        route='users/',
        view=include('users.urls', namespace='users'),
    ),
    # path(
    #     route='categories/',
    #     view=include(...),
    #     name='categories'
    # ),
    # path(
    #     route='products/',
    #     view=include(...),
    #     name='products'
    # ),
    # path(
    #     route='orders/',
    #     view=include(...),
    #     name='orders'
    # ),

    # API


    # Core
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls)
]

urlpatterns += staticfiles_urlpatterns()
