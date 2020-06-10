from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect

from accounts.models import Vendor
from photos.models import Album
from users.decorators import vendor_required
from catalog.forms import (ProductForm,
                           PriceForm,
                           DimensionForm,
                           ProductAttributeForm,
                           ProductDetailsForm,
                           ProductStockForm)
from catalog.models import Product, PredefineAttributeValue, ProductAttribute

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

@login_required
@vendor_required
def product_attributes(request, slug):
    template_name = 'products/product_attribute.html'
    context = {}

    if slug is None or slug == "":
        return redirect('not-found')

    product = Product.objects.get(slug=slug)

    if product is None:
        return redirect('not-found')

    if not product.vendor == request.user.vendor:
        return redirect('forbidden')
    
    attributes = ProductAttribute.objects.all()

    # if request.method == 'POST':
    #     form = ProductAttributeForm(request.POST or None, instance=product)
    #     if form.is_valid():
    #         form.save()
    #         return redirect(product.get_attribute_url())
    # else:
    #     form = ProductAttributeForm(instance=product)
    # context["form"] = form

    context["attributes"] = attributes
    context["product"] = product
    return render(request, template_name, context)

@login_required
@vendor_required
def set_attribute_values(request, slug):
    if slug is None or slug == "":
        return Http404

    product = Product.objects.get(slug=slug)

    if product is None:
        return Http404

    if request.method == "POST" and request.is_ajax():
        values = PredefineAttributeValue.objects.filter(id__in=request.POST.getlist('attribute_values'))
        product.attributes.clear()
        product.attributes.add(*values)
        data = {'success': True, 'message': 'Attributes added to product.'}
        return JsonResponse(data, status=200)