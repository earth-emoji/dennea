import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Vendor, Customer, Driver
from catalog.models import Product
from users.models import User

from .extras import generate_order_id
from .models import Order, OrderItem, Basket

def get_user_pending_order(request):
    # get order for the correct user
    customer = get_object_or_404(Customer, user=request.user)
    order = Order.objects.filter(customer=customer, is_fulfilled=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0

def get_vendor_pending_orders(request, slug):
    template_name = 'orders/vendor_pending_orders.html'
    vendor = get_object_or_404(Vendor, user=request.user, slug=slug)
    orders = OrderItem.objects.filter(vendor=vendor, is_ordered=True, is_fulfilled=False)
    data = {}
    data['orders'] = orders
    return render(request, template_name, data)

@login_required()
def get_driver_deliveries(request, slug):
    template_name = 'orders/driver_deliveries.html'
    driver = get_object_or_404(Driver, user=request.user, slug=slug)
    orders = OrderItem.objects.filter(driver=driver, is_fulfilled=False)
    data = {}
    data['orders'] = orders
    return render(request, template_name, data)

@login_required()
def get_pending_orders(request):
    template_name = 'orders/pending_orders.html'
    orders = OrderItem.objects.filter(is_fulfilled=False)
    data = {}
    data['orders'] = orders
    return render(request, template_name, data)

@login_required()
def get_customer_pending_orders(request, slug):
    template_name = 'orders/customer_pending_orders.html'
    customer = Customer.objects.get(slug=slug)
    orders = Order.objects.filter(customer=customer, is_fulfilled=False)
    data = {}
    data['orders'] = orders
    return render(request, template_name, data)

@login_required()
def get_order_details(request, slug):
    template_name = 'orders/order_details.html'
    context = {}
    order = Order.objects.get(slug=slug)
    context["order"] = order
    return render(request, template_name, context)

@login_required()
def get_customer_order_details(request, slug):
    template_name = 'orders/customer_order_details.html'
    order = Order.objects.get(slug=slug)
    data = {}
    data['order'] = order
    return render(request, template_name, data)

@login_required()
def get_vendor_order_details(request, slug):
    template_name = 'orders/vendor_order_details.html'
    order = OrderItem.objects.get(slug=slug, vendor=request.user.vendor)
    data = {}
    data['order'] = order
    return render(request, template_name, data)

@login_required()
def get_driver_order_details(request, slug):
    template_name = 'orders/driver_order_details.html'
    order = OrderItem.objects.get(slug=slug, driver=request.user.driver)
    data = {}
    data['order'] = order
    return render(request, template_name, data)

@login_required
def add_to_cart(request, slug):
    product = Product.objects.get(slug=slug)
    customer = get_object_or_404(Customer, user=request.user)

    customer.basket.add_to_basket(product)

    messages.info(request, "item added to cart")
    return redirect('products:product-list')

# @login_required()
# def add_to_cart(request, **kwargs):
#     # get the user profile
#     customer = get_object_or_404(Customer, user=request.user)
#     # filter products by id
#     product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
#     # check if the user already owns this product
#     # if product in request.user.profile.ebooks.all():
#     #     messages.info(request, 'You already own this ebook')
#     #     return redirect(reverse('products:product-list')) 
#     # create orderItem of the selected product
    
#     # create order associated with the user
#     user_order, status = Order.objects.get_or_create(customer=customer, is_fulfilled=False)
#     order_item, status = OrderItem.objects.get_or_create(order=user_order, product=product, vendor=product.vendor)
#     # user_order.items.add(order_item)
#     if status:
#         # generate a reference code
#         user_order.ref_code = generate_order_id()
#         user_order.save()

    # show confirmation message and redirect back to the same page
    # messages.info(request, "item added to cart")
    # return redirect('products:product-list')

@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect('shopping_cart:order_summary')


@login_required()
def order_details(request, template_name='shopping_cart/order_summary.html', **kwargs):
    customer = get_object_or_404(Customer, user=request.user)
    context = {
        'order': customer.basket
    }
    return render(request, template_name, context)

def purchase_success(request):
    # a view signifying the transcation was successful
    customer = Customer.objects.get(user=request.user)
    order = Order.objects.create(customer=customer, ref_code=generate_order_id())

    for item in customer.basket.get_cart_items():
        item.order = order
        item.is_ordered = True
        item.save()

        product = item.product
        product.sold = product.sold + 1
        product.stock_quantity = product.stock_quantity - 1
        product.save()

    customer.basket.empty_basket()
    
    return render(request, 'shopping_cart/purchase_success.html', {})