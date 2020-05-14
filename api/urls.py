from django.contrib import admin
from django.urls import path, include

from core.views import home_view, authorize

urlpatterns = [
    path('', home_view, name='home'),
    path('authorize/', authorize, name='authorize'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
