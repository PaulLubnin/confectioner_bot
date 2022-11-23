from email.policy import default
from operator import mod
from django.db import models
from datetime import datetime

class Layers(models.Model):
    quantity = models.IntegerField(verbose_name='Количество слоев')
    price = models.DecimalField(
        max_digits=None, 
        verbose_name='Цена', 
        decimal_places=2
        )

class Shapes(models.Model):
    shape = models.CharField(verbose_name='Форма коржа', max_length=32)
    price = models.DecimalField(
        max_digits=None, 
        verbose_name='Цена', 
        decimal_places=2
        )

class Toppings(models.Model):
    topping = models.CharField(verbose_name='Топпинги', max_length=32)
    price = models.DecimalField(
        max_digits=None, 
        verbose_name='Цена', 
        decimal_places=2
        )

class Berries(models.Model):
    berry = models.CharField(verbose_name='Ягоды', max_length=32)
    price = models.DecimalField(
        max_digits=None, 
        verbose_name='Цена', 
        decimal_places=2
        )

class Decorations(models.Model):
    decoration = models.CharField(verbose_name='Декор', max_length=32)
    price = models.DecimalField(
        max_digits=None, 
        verbose_name='Цена', 
        decimal_places=2
        )

class Cakes(models.Model):
    layers = models.ForeignKey(
        Layers, 
        verbose_name='Количество слоев', 
        on_delete=models.CASCADE
        )
    shapes = models.ForeignKey(
        Shapes, 
        verbose_name='Форма коржа', 
        on_delete=models.CASCADE
        )
    toppings = models.ForeignKey(
        Toppings, 
        verbose_name='Топпинги', 
        on_delete=models.CASCADE
        )
    berries = models.ForeignKey(
        Berries, 
        verbose_name='Ягоды', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE
        )
    decorations = models.ForeignKey(
        Decorations, 
        verbose_name='Декор', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE
        )
    description = models.TextField(verbose_name='Описание торта')
    picture = models.ImageField(verbose_name='Изображение торта')
    default = models.BooleanField(default=False)
    price = models.DecimalField(
        max_digits=None,
        verbose_name='Цена', 
        decimal_places=2
        )

class Clients(models.Model):
    name = models.CharField(max_length=32, verbose_name='Имя')
    phone = models.CharField(max_length=32, verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес')

class Orders(models.Model):
    client = models.ForeignKey(Clients, verbose_name='Клиент', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Комментарий к заказу')
    order_price = models.DecimalField(max_digits=None, verbose_name='Сумма заказа', decimal_places=2)
#    address = models.TextField()
#    time = models.DateTimeField(default=datetime.now())
#    deadline = models.DateTimeField()
#    urgency = models.BooleanField(default=False)

class OrderedCakes(models.Model):
    order = models.ForeignKey(Orders, verbose_name='Заказ', on_delete=models.CASCADE)
    cake = models.ForeignKey(Cakes, verbose_name='Торт', on_delete=models.CASCADE)
    sign = models.TextField(verbose_name='Надпись на торте')
