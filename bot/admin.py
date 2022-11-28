from django.contrib import admin

from .models import Order, Client, Cake, Layer, Shape, Topping, Berry, OrderedCake


@admin.register(OrderedCake)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order',)
    list_filter = ('order',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_time','order_price')
    list_filter = ('order_time',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('fio','phone', 'address')
    list_filter = ('address',)

@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('default',)

@admin.register(Layer)
class LayerAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'price')
    

@admin.register(Shape)
class ShapeAdmin(admin.ModelAdmin):
    list_display = ('shape', 'price')

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')

@admin.register(Berry)
class BerryAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')