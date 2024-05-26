from django.shortcuts import render
from rest_framework.response import Response
from django.db.models.aggregates import Count
from rest_framework.viewsets import(
    ModelViewSet,
    GenericViewSet
)
from store.models import(
    Category,
    Author,
    Publication,
    Book,
    Order,
    OrderItem,
    Customer
)
from store.serializers import(
    CategorySerializer,
    AuthorSerializer,
    PublicationSerializer,
    BookSerializer,
    CustomerSerializer,
    OrderSerializer
)

# Create your views here.

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(books_count=Count('book')).all()
    serializer_class = CategorySerializer

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class PublicationViewSet(ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer





