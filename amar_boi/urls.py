"""
URL configuration for amar_boi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
        Amar Boi is an online bookshop API developed using Django Rest Framework (DRF). It integrates djoser for user management,\
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

    path('amar-boi/', include('core.urls')),
    path('', include('store.urls')),
]
