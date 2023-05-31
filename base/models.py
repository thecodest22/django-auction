from django.db import models
from django.contrib.auth.models import User

from treebeard.mp_tree import MP_Node


class Category(MP_Node):
    """Категория товаров. Организовано в виде дерева с родительскими и дочерними категориями"""
    name = models.CharField(verbose_name='Название категории', max_length=50)

    node_order_by = ('name',)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Класс товара"""
    title = models.CharField(verbose_name='Наименование', max_length=200)
    picture = models.ImageField(verbose_name='Изображение товара', blank=True, default="/img/default_prod_img.png",
                                upload_to="img")
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2)
    description = models.TextField(verbose_name='Описание', blank=True, default='')
    vendor = models.CharField(verbose_name='Производитель', max_length=200, blank=True, default='')
    rating = models.DecimalField(verbose_name='Рейтинг', max_digits=12, decimal_places=2, default=0)
    reviews_num = models.PositiveSmallIntegerField(verbose_name='Количество отзывов', default=0)
    stock_quantity = models.PositiveSmallIntegerField(verbose_name='Количество на складе', default=0)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    # offer_id = models.BigAutoField(primary_key=True, editable=False)
    # category = models.CharField(verbose_name='Категория', max_length=200, blank=True, default='')
    category = models.ForeignKey(verbose_name='Категория', to=Category, on_delete=models.CASCADE,
                                 related_name='products', related_query_name='product')
    customer = models.ForeignKey(verbose_name='Пользователи', to=User, on_delete=models.SET_NULL, null=True,
                                 related_name='products', related_query_name='product')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.title} | {self.vendor} | {self.price}'


class Review(models.Model):
    """Класс отзыва"""
    title = models.CharField(verbose_name='Заголовок', max_length=200, blank=True, default='')
    rating = models.PositiveSmallIntegerField(verbose_name='Оценка', default=0)
    comment = models.TextField(verbose_name='Комментарий', blank=True, default='')
    created_at = models.DateTimeField(verbose_name='Добавлен', auto_now_add=True)
    # _id = models.AutoField(primary_key=True, editable=False)
    to_product = models.ForeignKey(verbose_name='На товар', to=Product, on_delete=models.CASCADE,
                                   related_name='reviews', related_query_name='review')
    reviewer = models.ForeignKey(verbose_name='Отзыв оставил', to=User, on_delete=models.SET_NULL, null=True,
                                 related_name='reviews', related_query_name='review')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return str(self.rating)


class Order(models.Model):
    """Класс заказа"""
    payment_method = models.CharField(verbose_name='Способ оплаты', max_length=200, blank=True, default='')
    tax = models.DecimalField(verbose_name='Налог', max_digits=4, decimal_places=2, default=0)
    delivery_cost = models.DecimalField(verbose_name='Стоимость доставки', max_digits=8, decimal_places=2, default=0)
    total_cost = models.DecimalField(verbose_name='Итоговая стоимость', max_digits=9, decimal_places=2, default=0)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    is_paid = models.BooleanField(verbose_name='Оплачен', default=False)
    paid_at = models.DateTimeField(verbose_name='Дата и время оплаты', null=True, blank=True, editable=False)
    is_delivered = models.BooleanField(verbose_name='Доставлен', default=False)
    delivered_at = models.DateTimeField(verbose_name='Дата и время доставки', null=True, blank=True, editable=False)
    # _id = models.AutoField(primary_key=True, editable=False)
    customer = models.ForeignKey(verbose_name='Покупатель', to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.created_at)


class OrderItem(models.Model):
    """Класс позиции заказа"""
    title = models.CharField(verbose_name='Имя', max_length=200)
    product = models.ForeignKey(verbose_name='Товар', to=Product, on_delete=models.CASCADE, related_name='order_items',
                                related_query_name='order_item')
    order = models.ForeignKey(verbose_name='В заказе', to=Order, on_delete=models.CASCADE, related_name='order_items',
                              related_query_name='order_item')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')
    price = models.DecimalField(verbose_name='Цена', max_digits=12, decimal_places=2)
    # image = models.CharField(max_length=200, null=True, blank=True)
    # _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return self.title


class DeliveryAddress(models.Model):
    """Класс адреса доставки"""
    address = models.CharField(verbose_name='Улица, дом, квартира', max_length=100)
    city = models.CharField(verbose_name='Город', max_length=30)
    postal_code = models.CharField(verbose_name='Почтовый индекс', max_length=10, blank=True, default='')
    country = models.CharField(verbose_name='Страна', max_length=20)
    delivery_cost = models.DecimalField(verbose_name='Стоимость доставки', max_digits=8, decimal_places=2, default=0)
    # _id = models.AutoField(primary_key=True, editable=False)
    order = models.OneToOneField(verbose_name='Заказ', to=Order, on_delete=models.CASCADE, blank=True,
                                 related_name='delivery_address')

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'

    def __str__(self):
        return str(self.address)
