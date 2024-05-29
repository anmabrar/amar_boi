from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers
from .import views


router = routers.DefaultRouter()

router.register('categories', views.CategoryViewSet)
router.register('authors', views.AuthorViewSet)
router.register('publications', views.PublicationViewSet)
router.register('books', views.BookViewSet, basename='books')
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet)
router.register('carts', views.CartViewSet)

books_router = routers.NestedDefaultRouter(router, 'books', lookup='book')
books_router.register('reviews', views.ReviewViewSet, basename='book-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')


urlpatterns = router.urls + books_router.urls + carts_router.urls