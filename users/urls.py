from rest_framework import routers

from users.apps import UsersConfig
from users.views import PayList

router = routers.DefaultRouter()
router.register(r'payment', PayList)
app_name = UsersConfig.name
urlpatterns = router.urls
