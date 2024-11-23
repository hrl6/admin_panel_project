from django.contrib import admin
from .models import Product, Order

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ('name', 'price', 'stock', 'stock_status', 'created_at')
  list_editable = ('price', 'stock')
  search_fields = ('name', 'description')
  list_filter = ('created_at', 'stock')
  list_per_page = 10

  def stock_status(self, obj):
    if obj.stock == 0:
      return 'Out of Stock'
    elif obj.stock < 10:
      return 'Low Stock'
    return 'In Stock'
  stock_status.short_description = 'Stock Status'

  actions = ['mark_as_out_of_stock']

  def mark_as_out_of_stock(self, request, queryset):
    queryset.update(stock=0)
  mark_as_out_of_stock.short_description = "Mark selected products as out of stock"

  @admin.register(Order)
  class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'status', 'total_amount', 'created_at', 'customer_email')
    list_editable = ('status',)
    search_fields = ('order_number', 'customer_name', 'customer_email')
    list_filter = ('status', 'created_at')
    list_per_page = 10

    fieldsets = (
      ('Order Information', {
        'fields': ('status', 'total_amount', 'notes')
      }),
      ('Customer Details', {
        'fields': ('customer_name', 'customer_email')
      }),
    )

    actions = ['mark_as_completed', 'mark_as_processing']

    def mark_as_completed(self, queryset):
      queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected orders as completed"

    def mark_as_processing(self, queryset):
      queryset.update(status='processing')
    mark_as_processing.short_description = "Mark selected orders as processing"

