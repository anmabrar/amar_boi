from django.contrib import admin
from django.urls import path,include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Amar Boi",
      default_version='v1',
      description="""
        Amar Boi is an online bookshop API developed using Django Rest Framework (DRF). It integrates user management,\
        JWT for secure authentication, and django_filters for advanced filtering capabilities. Utilizing nested routers, it organizes \
        various endpoints for seamless navigation. The API supports comprehensive models, including Category, Author, Publication, Book, \
        Order, OrderItem, Customer, Review, Cart, and CartItem. This setup ensures a robust and scalable system, facilitating efficient \
        management of books, orders, and customer interactions, delivering a streamlined and engaging user experience.
        """,
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


admin.site.site_header = "Amar Boi"
admin.site.index_title = "Admin"
admin.site.site_title = "Amar Boi"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("__debug__/", include("debug_toolbar.urls")),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('', include('core.urls'), name='user'),
    path('', include('store.urls')),
]
