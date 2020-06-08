from django.urls import include, path

from accounts import views

urlpatterns = [
    path('vendors/', include(([
        path('<slug:slug>/', views.dashboard, name='dashboard'),
    ], 'vendors'))),
]