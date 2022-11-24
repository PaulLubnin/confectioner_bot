from django.db import models



class Order(models.Model):
    client = models.ForeignKey(
        'Client',
        verbose_name='клиент',
        related_name='orders',
        on_delete=models.CASCADE,
     )
    cakes = models.ManyToManyField(
        'Cake',
        verbose_name='торты',
        related_name='orders',
     )
    comment = models.TextField(
        'комментарий к заказу',
        blank=True,
     )
    order_price = models.DecimalField(max_digits=19, verbose_name='Сумма заказа', decimal_places=2)
    #    address = models.TextField()
    order_time = models.DateTimeField(verbose_name='время создания', auto_now_add=True)
    #    deadline = models.DateTimeField()
    #    urgency = models.BooleanField(default=False)

    def __str__(self):
        return f'{str(self.order_time)}'    


class Client(models.Model):
    fio = models.CharField('клиент', max_length=200)
    phone = models.CharField('клиент', max_length=12)
    address = models.TextField(
        'Адрес квартиры',
        help_text='ул. Подольских курсантов д.5 кв.4'
     )

    def __str__(self):
        return self.fio    

class Cake(models.Model):
    title = models.CharField('название торта', max_length=200, blank=True)
    description = models.TextField(
        'описание торта',
        blank=True,
     )
    picture = models.ImageField(
        verbose_name='изображение торта',
        blank=True,
        null=True,
     )
    default = models.BooleanField('торт в ассортименте', default=False)
    layers = models.ForeignKey(
        'Layer',
        verbose_name='слои',
        related_name='cakes',
        null=True,
        on_delete=models.SET_NULL,
     )
    shape = models.ForeignKey(
        'Shape',
        verbose_name='форма',
        related_name='cakes',
        null=True,
        on_delete=models.SET_NULL,
     )
    
    toppings = models.ManyToManyField(
        'Topping',
        verbose_name='топинги',
        related_name='cakes',
     )
    berries = models.ManyToManyField(
        'Berry',
        verbose_name='ягоды',
        related_name='cakes',
     )

    def __str__(self):
        return self.title    
    
class Layer(models.Model):
    quantity = models.IntegerField(verbose_name='Количество слоев')
    price = models.DecimalField(
        max_digits=19, 
        verbose_name='Цена', 
        decimal_places=2,
        )

    def __str__(self):
        return f'{str(self.quantity)}'    

class Shape(models.Model):
    shape = models.CharField(verbose_name='Форма коржа', max_length=32)
    price = models.DecimalField(
        max_digits=19, 
        verbose_name='Цена', 
        decimal_places=2
        )

    def __str__(self):
        return self.shape    

class Topping(models.Model):
    title = models.CharField(verbose_name='Топпинг', max_length=32)
    price = models.DecimalField(
        max_digits=19, 
        verbose_name='Цена', 
        decimal_places=2
        )

    def __str__(self):
        return self.title    

class Berry(models.Model):
    title = models.CharField(verbose_name='Ягода', max_length=32)
    price = models.DecimalField(
        max_digits=19, 
        verbose_name='Цена', 
        decimal_places=2
        )

    def __str__(self):
        return self.title    
