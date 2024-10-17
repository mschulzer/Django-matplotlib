from django.urls import path
from .views import home_view, plot_view

urlpatterns = [
    path('', home_view, name="home-view"),
    path('plot/', plot_view, name='plot_view'),
]