from django.urls import path, include

from .views import (
    add_to_cart,
    delete_from_cart,
    order_details,
    purchase_success,
    get_vendor_pending_orders,
    get_pending_orders,
    get_customer_pending_orders,
    get_driver_deliveries,
    get_order_details,
    get_customer_order_details,
    get_vendor_order_details,
    get_driver_order_details,
)

urlpatterns = [
    path('cart/', include(([
        path('add-to-cart/<slug:slug>/', add_to_cart, name="add_to_cart"),
        path('order-summary/', order_details, name="order_summary"),
        path('success/', purchase_success, name='purchase_success'),
        path('item/delete/<int:item_id>/', delete_from_cart, name='delete_item'),
    ], 'shopping_cart'), namespace='shopping_cart')),
    path('orders/', include(([
        path('', get_pending_orders, name="orders"),
        path('vendor/<slug:slug>/', get_vendor_pending_orders, name='vendor-orders'),
        path('customer/<slug:slug>/', get_customer_pending_orders, name='customer-orders'),
        path('driver/<slug:slug>/', get_driver_deliveries, name='driver-orders'),
        path('<uuid:slug>/details', get_order_details, name='order-details'),
        path('<uuid:slug>/customer-details', get_customer_order_details, name='customer-details'),
        path('<uuid:slug>/vendor-details', get_vendor_order_details, name='vendor-details'),
        path('<uuid:slug>/delivery-details', get_driver_order_details, name='driver-details'),
    ], 'orders'), namespace='orders')),
]

