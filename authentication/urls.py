from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'authentication'

router = DefaultRouter()
router.register('email', views.EmailSender, basename='confirmation')
router.register('token', views.TokenAuthorization, basename='token')

urlpatterns = [
    path('v1/auth/', include(router.urls))
]
