from _decimal import Decimal

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.handlers.wsgi import WSGIRequest

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import *
from base.serializers import ProductSerializer


@api_view(['GET'])
def get_products(request: WSGIRequest) -> Response:
    query = request.query_params.get('keyword', '')
    products = Product.objects.filter(title__icontains=query, stock_quantity__gte=1)  #.order_by('-_id')
    page = int(request.query_params.get('page', 1))
    paginator = Paginator(products, 8)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    serializer = ProductSerializer(products, many=True)

    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
def get_top_products(request: WSGIRequest) -> Response:
    products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def get_product(request: WSGIRequest, pk) -> Response:
    product = Product.objects.get(pk=pk)
    serializer = ProductSerializer(product, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_product(request):
    user = request.user
    category = Category.objects.get()
    product = Product.objects.create(
        customer=user,
        title="Test Product Name",
        price=0,
        vendor="Test Brand",
        category=category,
    )

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_product(request, pk):
    data = request.data
    product = Product.objects.get(pk=pk)
    category = data["category"]

    product.title = data["name"]
    product.price = data["price"] * 1.1
    product.vendor = data["brand"]
    product.stock_quantity = data["countInStock"]
    product.category = category
    product.description = data["description"]
    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_product(request: WSGIRequest, pk: int) -> Response:
    product = Product.objects.get(pk=pk)
    product.delete()
    return Response("Product deleted successfully")


@api_view(['POST'])
def upload_image(request: WSGIRequest) -> Response:
    data = request.data
    product_id = data['product_id']
    image_file = request.FILES.get('image')
    if image_file:
        product = Product.objects.get(pk=product_id)
        product.picture.save(image_file.name, image_file, save=True)
        return Response('Image was successfully uploaded')
    return Response('No images were passed!')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product_review(request: WSGIRequest, pk: int) -> Response:
    user = request.user
    data = request.data
    product = Product.objects.get(pk=pk)
    reviews = product.reviews.all()

    # 1. Если отзыв уже оставлен данным пользователем:
    if reviews.filter(user=user).exists():
        content = {'detail': 'You have already reviewed this product'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 2. Если рейтинг поставлен нулевой:
    if data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3. Если все норм, создаем отзыв и добавляем к товару:
    review = Review.objects.create(
        reviewer=user,
        to_product=product,
        title=user.first_name,
        rating=data['rating'],
        comment=data['comment'],
    )

    product.reviews_num = reviews.count()
    summary_rating = reviews.aggregate(models.Sum('rating')).get('rating__sum')
    product.rating = summary_rating / product.reviews_num
    product.save()

    return Response('Review Added')


@api_view(['PUT'])
def increase_price(request: WSGIRequest, pk: int) -> Response:
    product = Product.objects.get(pk=pk)
    product.price *= Decimal(1.1)
    product.save(update_fields='price')
    serializer = ProductSerializer(product, many=False)

    return Response(serializer.data)
