from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import index_view, add_file_view, show_file_view, delete_view, delete_file, add_directory_view, delete_directory

app_name = 'app'
urlpatterns = [
    path('', index_view, name='index'),
    path('add_file/', add_file_view, name='add_file'),
    path('add_directory/', add_directory_view, name='add_directory'),
    path('show_file/<str:name>/', show_file_view, name='show_file'),
    path('delete/', delete_view, name='delete'),
    path('delete_file/', delete_file, name='delete_file'),
    path('delete_directory/', delete_directory, name='delete_directory'),
]