from rest_framework import routers
from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register('user/register', views.UserRegisterViewSet, basename='user-register')
router.register('user/login', views.UserLoginViewSet, basename='user-login')
router.register('users', views.UserViewSet)


urlpatterns = router.urls