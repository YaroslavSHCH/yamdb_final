from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'users'

router = DefaultRouter()
router.register('users', views.UsersView)

urlpatterns = [
    path('v1/', include(router.urls)),
]
