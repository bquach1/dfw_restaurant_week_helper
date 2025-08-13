from django.urls import path
from . import views

urlpatterns = [
    path("google_places/", views.get_restaurant_info, name="google_places"),
]
