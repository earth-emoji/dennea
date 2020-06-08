from django.shortcuts import redirect, render

from accounts.models import Vendor

def dashboard(request, slug):
    template_name = 'vendors/dashboard.html'
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
