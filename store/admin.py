from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .import models

# Register your models here.

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'books_count']
    search_fields = ['name']

    @admin.display(ordering='books_count')
    def books_count(self, category):
        url = (
            reverse('admin:store_book_changelist')
            + '?'
            + urlencode({
                'category__id': str(category.id)
            }))
        return format_html('<a href="{}">{}</a>',url, category.books_count)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            books_count=Count('book')
        )
         

@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'date_of_birth', 'nationality', 'is_alive']
    list_per_page = 20
    list_filter = ['nationality']
    search_fields = ['first_name', 'last_name']


@admin.register(models.Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['name','address','website', 'email', 'phone_number','established_date']
    list_per_page = 20
    search_fields = ['name']


class PriceFilter(admin.SimpleListFilter):
    title = 'price'
    parameter_name = 'price'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('<12', 'Low'),
            ('<15', 'Medium'),
            ('>15', 'High')
        ]
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<12':
            return queryset.filter(price__lt=12)
        elif self.value() == '<15':
            return queryset.filter(price__lt=15)
        elif self.value() == '>15':
            return queryset.filter(price__gt=15)



@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    actions = ['clear_stock']
    prepopulated_fields = {
         'slug': ['title']
    }
    autocomplete_fields = ['author', 'category', 'publication']
    list_display = ['title', 'author', 'category', 'publication', 'price', 'stock', 'inventory_status']
    search_fields = ['title', 'author', 'category', 'publication']
    list_filter = ['category', 'last_update', PriceFilter]
    list_editable = ['price', 'stock']
    list_select_related = ['author','category', 'publication']
    list_per_page = 10

    @admin.display(ordering='stock')
    def inventory_status(self,book):
        if book.stock < 80:
            return 'LOW'
        return 'OK'
    
    @admin.action(description='Clear stock')
    def clear_stock(self, request, queryset:QuerySet):
        updated_count = queryset.update(stock=0)
        self.message_user(
            request,
            f'{updated_count} books stock ware successfully updated.',
            messages.ERROR
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_select_related = ['user']
    list_editable = ['membership']
    list_filter = ['membership']
    # ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_per_page = 10


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['book']
    model = models.OrderItem
    min_num = 1
    max_num = 10
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer', 'payment_status']
    list_filter = ['payment_status']
    inlines = [OrderItemInline]
    list_per_page = 10