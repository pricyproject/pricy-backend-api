from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

"""restoxa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Restoxa Admin Panel'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', include("products.urls")),
    path('api/product-groups/', include("product_groups.urls")),
    path('api/product-categories/', include("product_categories.urls")),
    path('api/shops/', include("shops.urls")),
    path('api/discovers/', include("discovers.urls")),
    # API Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI:
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc UI:
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
