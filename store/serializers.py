from rest_framework import serializers
from decimal import Decimal
from store.models import (
    Category,
    Author,
    Publication,
    Book,
    Customer,
    Order,
    OrderItem,
    Review,
    Cart,
    CartItem
)


class CategorySerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'books_count']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'slug',
            'author',
            'category',
            'publication',
            'unit_price',
            'price_with_tax',
            'stock',
            'description',

        ]
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
        
    def calculate_tax(self, book:Book):
        return book.unit_price * Decimal(1.1)
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'date',
            'name',
            'description'
        ]
    
    def create(self, validated_data):
        book_id = self.context['book_id']
        return Review.objects.create(book_id=book_id, **validated_data) 

class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item:CartItem):
        return cart_item.quantity * cart_item.book.unit_price
    class Meta:
        model = CartItem
        fields = ['id', 'book', 'quantity', 'total_price' ]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart:Cart):
        return sum([item.quantity * item.book.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

class AddCartItemSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField()

    def validate_book_id(self, value):
        if not Book.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No book with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        book_id = self.validated_data['book_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, book_id=book_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        
        return self.instance
    class Meta:
        model = CartItem
        fields = ['id', 'book_id', 'quantity']

    

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    