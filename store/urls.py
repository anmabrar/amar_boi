from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .import views


router = DefaultRouter()

router.register('category', views.CategoryViewSet)
router.register('author', views.AuthorViewSet)
router.register('publication', views.PublicationViewSet)
router.register('book', views.BookViewSet)
router.register('customer', views.CustomerViewSet)
router.register('order', views.OrderViewSet)

urlpatterns = router.urls