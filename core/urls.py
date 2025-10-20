"""
URL configuration for core project.

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
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # Django Admin Panel
    path("admin/", admin.site.urls),

    # API v1 - This is where you will include your app's URLs later
    # Example: path('api/v1/', include('users.urls')),

    # API Documentation Routes (drf-spectacular)
    # Serves the OpenAPI 3.0 schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI endpoints:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Prometheus metrics endpoint (django-prometheus)
    # This will expose a /metrics endpoint
    path('', include('django_prometheus.urls')),
]
