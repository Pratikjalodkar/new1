from django.urls import path
from .views import (
    signup,
    signin,
    add_product,
    update_product,
    delete_product,
    get_all_products,
    add_product_to_cart,
    update_cart,
    delete_product_from_cart,
    get_cart,
    place_order,
    get_all_orders,
    get_orders_by_customer,
)

urlpatterns = [
    # User authentication
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),

    # Product management
    path('addproduct/', add_product, name='add_product'),
    path('updateproduct/<int:productId>/', update_product, name='update_product'),
    path('deleteproduct/<int:productId>/', delete_product, name='delete_product'),
    path('products/', get_all_products, name='get_all_products'),

    # Cart management
    path('cart/add/', add_product_to_cart, name='add_product_to_cart'),
    path('cart/update/', update_cart, name='update_cart'),
    path('cart/delete/', delete_product_from_cart, name='delete_product_from_cart'),
    path('cart/', get_cart, name='get_cart'),

    # Order management
    path('placeorder/', place_order, name='place_order'),
    path('getallorders/', get_all_orders, name='get_all_orders'),
    path('orders/customer/<int:customerId>/', get_orders_by_customer, name='get_orders_by_customer'),
]