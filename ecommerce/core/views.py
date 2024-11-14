from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import IsAuthenticated
from .models import Product, Cart, CartItem, Order
from .serializers import ProductSerializer, CartItemSerializer, OrderSerializer
from .permissions import IsAdminUser   
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken


class OrderPagination(PageNumberPagination):
    page_size = 10  

@api_view(['POST'])
def signup(request):
    data = request.data
    if User.objects.filter(email=data['email']).exists():
        return Response({"message": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

    user = User(
        username=data['email'],
        email=data['email'],
        password=make_password(data['password'])
    )
    user.save()
    return Response({"message": "Signup successful", "user_id": user.id}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def signin(request):
    data = request.data
    try:
        user = User.objects.get(email=data['email'])
        if check_password(data['password'], user.password):
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "user_id": user.id,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"message": "User  not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    # Admin only
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        product = serializer.save()
        return Response({"message": "Product added", "product_id": product.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser ])
def update_product(request, productId):
    try:
        product = Product.objects.get(id=productId)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser ])
def delete_product(request, productId):
    try:
        product = Product.objects.get(id=productId)
        product.delete()
        return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_all_products(request):
    products = Product.objects.all()
    if not products:
        return Response({"message": "No products found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product_to_cart(request):
    user = request.user
    data = request.data
    cart, created = Cart.objects.get_or_create(user=user)

    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if quantity <= 0:
        return Response({"message": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()
        return Response({"message": "Product added to cart", "cart_item": CartItemSerializer(cart_item).data}, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart(request):
    user = request.user
    data = request.data
    product_id = data.get('product_id')
    new_quantity = data.get('quantity')

    try:
        cart = Cart.objects.get(user=user)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)

        if new_quantity < 0:
            return Response({"message": "Quantity cannot be negative."}, status=status.HTTP_400_BAD_REQUEST)

        if new_quantity == 0:
            cart_item.delete()
            return Response({"message": "Product removed from cart."}, status=status.HTTP_200_OK)

        cart_item.quantity = new_quantity
        cart_item.save()
        return Response({"message": "Cart updated", "cart_item": CartItemSerializer(cart_item).data}, status=status.HTTP_200_OK)

    except Cart.DoesNotExist:
        return Response({"message": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
    except CartItem.DoesNotExist:
        return Response({"message": "Product not found in cart."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product_from_cart(request):
    user = request.user
    data = request.data
    product_id = data.get('product_id')

    try:
        cart = Cart.objects.get(user=user)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()
        return Response({"message": "Product removed from cart."}, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({"message": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
    except CartItem.DoesNotExist:
        return Response({"message": "Product not found in cart."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
        cart_items = cart.items.all()
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        return Response({"items": CartItemSerializer(cart_items, many=True).data, "total_amount": total_amount}, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({"message": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    user = request.user
    data = request.data
    shipping_address = data.get('shipping_address')

    try:
        cart = Cart.objects.get(user=user)
        cart_items = cart.items.all()

        if not cart_items:
            return Response({"message": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=user, shipping_address=shipping_address)
        for item in cart_items:
            item.delete() 

        return Response({"message": "Order placed successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)
    except Cart.DoesNotExist:
        return Response({"message": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminUser ])
def get_all_orders(request):
    orders = Order.objects.all()
    paginator = OrderPagination()
    paginated_orders = paginator.paginate_queryset(orders, request)

    if not paginated_orders:
        return Response({"message": "No orders found."}, status=status.HTTP_404_NOT_FOUND)

    order_data = []
    for order in paginated_orders:
        order_data.append({
            "order_id": order.id,
            "user_id": order.user.id,
            "shipping_address": order.shipping_address,
            "created_at": order.created_at,
        })
    return paginator.get_paginated_response(order_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders_by_customer(request, customerId):
    try:
        orders = Order.objects.filter(user_id=customerId)
        if not orders:
            return Response({"message": "No orders found for this customer."}, status=status.HTTP_404_NOT_FOUND)

        order_data = []
        for order in orders:
            order_data.append({
                "order_id": order.id,
                "shipping_address": order.shipping_address,
                "created_at": order.created_at,
            })
        return Response(order_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"message": "User  not found."}, status=status.HTTP_404_NOT_FOUND)
    


