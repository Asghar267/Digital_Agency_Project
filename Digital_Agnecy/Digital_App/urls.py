"""
URL configuration for Digital_Agency project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import include, path
from . import views
from django.conf.urls.static import static

# app_name = 'Digital_App'


urlpatterns = [
    path('', views.service_list, name='service_list'),

    path('products/<int:service_id>', views.service_detail, name='service_detail'),
    path('service/<int:service_id>/add_to_cart/',views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
 
 
    path('register/', views.register_user, name='register_user'),
    path('signin/', views.loginUser, name='login_user'),
    path('logout/', views.logoutUser, name='logout_user'),
    path('profile', views.profileUser, name='profile_user'),

    path('cart/add/<int:service_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:service_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('search', views.search, name='search'),
 
 
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
