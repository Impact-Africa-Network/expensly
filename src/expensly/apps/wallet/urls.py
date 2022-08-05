from django.db import router
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.WalletModelViewSet, basename="wallet")


app_name = 'wallet'

urlpatterns = [
]
urlpatterns += router.urls