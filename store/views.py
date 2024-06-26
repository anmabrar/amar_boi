from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models.aggregates import Count
from store.permissions import IsAdminOrReadOnly
from rest_framework.permissions import(
    IsAuthenticated,
    IsAdminUser
)
from rest_framework.mixins import(
    CreateModelMixin,
    RetrieveModelMixin, 
    DestroyModelMixin,
)
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
    Customer,
    Review,
    Cart,
    CartItem
)
from store.serializers import(
    CategorySerializer,
    AuthorSerializer,
    PublicationSerializer,
    BookSerializer,
    CustomerSerializer,
    OrderSerializer,
    ReviewSerializer,
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    CreateOrderSerializer,
    UpdateOrderSerializer
)
from store.filters import BookFilter
from store.pagination import DefaultPagination


# Create your views here.

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(books_count=Count('books')).all()
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Book.objects.filter(category_id=kwargs['pk']).count() > 0 :
            return Response(
                {'error': 'Category cannot be deleted because it includes one or more Books.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
  

class PublicationViewSet(ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
   

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'description'] 
    ordering_fields = ['unit_price', 'last_update']


    def get_serializer_context(self):
        return {'request':self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(book_id=kwargs['pk']).count() > 0 : 
            return Response(
                {'error':'Book cannot be deleted because it is associated with an order item.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs['book_pk'])

    def get_serializer_context(self):
        return {'book_id':self.kwargs['book_pk']}
    
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__book').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer

    # method name write in lowercase otherwise not work
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('book')
 


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return[IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id':self.request.user.id}

        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        
        customer_id = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)



