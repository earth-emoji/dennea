from django.urls import include, path

from catalog import views

urlpatterns = [
    path('products/', include(([
        path('create/', views.create_product, name='create-product'),
        path('<slug:slug>/details', views.product_details, name='product-details'),
        path('<slug:slug>/price', views.product_price, name='product-price'),
        path('vendor/<slug:slug>/', views.vendor_products, name='vendor-products'),
    ], 'products'))),
]