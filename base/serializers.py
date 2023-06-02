from django.db.models import fields
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    is_staff = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'is_staff']

    def get_id(self, obj: User) -> int:
        return obj.id

    def get_is_staff(self, obj: User) -> bool:
        return obj.is_staff

    def get_name(self, obj: User) -> str:
        return obj.first_name or obj.email or obj.username


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'is_staff', 'token']

    def get_token(self, obj: User) -> str:
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_reviews(self, obj: Product):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


# class ShippingAddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ShippingAddress
#         fields = '__all__'
#
#
# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = '__all__'
#
#
# class OrderSerializer(serializers.ModelSerializer):
#     orderItems = serializers.SerializerMethodField(read_only=True)
#     shippingAddress = serializers.SerializerMethodField(read_only=True)
#     User = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = Order
#         fields = '__all__'
#
#     def get_orderItems(self, obj):
#         items = obj.orderitem_set.all()
#         serializer = OrderItemSerializer(items, many=True)
#         return serializer.data
#
#     def get_shippingAddress(self, obj):
#         try:
#             address = ShippingAddressSerializer(obj.shippingaddress,
#                                                 many=False).data
#         except:
#             address = False
#         return address
#
#     def get_User(self, obj):
#         items = obj.user
#         serializer = UserSerializer(items, many=False)
#         return serializer.data
