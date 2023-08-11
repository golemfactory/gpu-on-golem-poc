from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_data),
    path('all_clusters/', views.get_clusters_data),
    path('post_cluster/', views.post_clusters_object)
]