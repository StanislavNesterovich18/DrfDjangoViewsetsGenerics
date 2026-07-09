from django.urls import path
from rest_framework import routers
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    CreateApiView,
    PayList,
    UserDestroyAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
)

router = routers.DefaultRouter()
router.register(r"payment", PayList)
app_name = UsersConfig.name
urlpatterns = [
    path("registration/", CreateApiView.as_view(), name="Create_user"),
    path("retrieve/<int:pk>/", UserRetrieveAPIView.as_view(), name="Retrieve_user"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="Update_user"),
    path("destroy/<int:pk>/", UserDestroyAPIView.as_view(), name="Destroy_user"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
urlpatterns += router.urls
