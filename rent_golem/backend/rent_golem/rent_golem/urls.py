from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/v1/clusters/', include('clusters.urls')),
    path('api/v1/accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]