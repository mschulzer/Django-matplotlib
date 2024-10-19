from django.urls import path
from .views import home_view, plot_view, post_data_view, upload_data_view

urlpatterns = [
    path('', home_view, name="home-view"),
    path('plot/', plot_view, name='plot-view'),
    path('post/', post_data_view, name="post-data-view"),
    path('upload/', upload_data_view, name="upload-data-view"),
]