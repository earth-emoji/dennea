from django.shortcuts import render, redirect

# Create your views here.
def home(request, template_name='pages/home.html'):
    if request.user.is_authenticated:
        if request.user.is_member:
            return redirect('members:index')
    return render(request, template_name)
