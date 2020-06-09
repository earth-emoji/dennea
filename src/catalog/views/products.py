from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.models import Vendor
from photos.models import Album
from users.decorators import vendor_required
from catalog.forms import (ProductForm,
                           PriceForm,
                           DimensionForm,
                           ProductDetailsForm,
                           ProductStockForm)
from catalog.models import Product

@login_required
@vendor_required
def vendor_products(request, slug):
    template_name = 'products/vendor_products.html'
    context = {}

    if slug is None or slug == "":
        return redirect('not-found')

    vendor = Vendor.objects.get(slug=slug)

    if vendor is None:
        return redirect('not-found')

    if not vendor.user == request.user:
        return redirect('forbidden')

    context["vendor"] = vendor

    return render(request, template_name, context)

@login_required
@vendor_required
def create_product(request):
    template_name = 'products/create_product.html'
    context = {}
    if request.method == 'POST':
        form = ProductForm(request.POST or None)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.acl = request.user.acl
            product.save()
            Album.objects.create(name=product.name, owner=request.user)
            return redirect(product.get_absolute_url())
    else:
        form = ProductForm()
    context["form"] = form
    return render(request, template_name, context)

@login_required
@vendor_required
def product_details(request, slug):
    template_name = 'products/product_details.html'
    context = {}

    if slug is None or slug == "":
        return redirect('not-found')

    product = Product.objects.get(slug=slug)

    if product is None:
        return redirect('not-found')

    if not product.vendor == request.user.vendor:
        return redirect('forbidden')

    if request.method == 'POST':
        form = ProductDetailsForm(request.POST or None, instance=product)
        if form.is_valid():
            form.save()
            return redirect(product.get_absolute_url())
    else:
        form = ProductDetailsForm(instance=product)
    context["form"] = form
    context["product"] = product
    return render(request, template_name, context)

@login_required
@vendor_required
def product_price(request, slug):
    template_name = 'products/product_price.html'
    context = {}

    if slug is None or slug == "":
        return redirect('not-found')

    product = Product.objects.get(slug=slug)

    if product is None:
        return redirect('not-found')

    if not product.vendor == request.user.vendor:
        return redirect('forbidden')

    if request.method == 'POST':
        form = PriceForm(request.POST or None, instance=product)
        if form.is_valid():
            form.save()
            return redirect(product.get_price_url())
    else:
        form = PriceForm(instance=product)
    context["form"] = form
    context["product"] = product
    return render(request, template_name, context)