from django.shortcuts import render, redirect

# Create your views here.
def home(request, template_name='pages/home.html'):
    if request.user.is_authenticated:
        if request.user.is_vendor:
            return redirect('vendors:dashboard', request.user.vendor.slug)
    return render(request, template_name)
