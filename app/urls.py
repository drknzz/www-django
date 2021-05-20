from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# from .views import index_view, add_file_view, show_file_view, delete_view, delete_file, add_directory_view, delete_directory, show_tab, save_prover, save_vcs, compile, auth_user
from .views import index_view, add_file_view, add_directory_view, show_tab, save_prover, save_vcs, auth_user
from .views import js_show_file, js_delete_file, js_delete_directory, js_compile

app_name = 'app'
urlpatterns = [
    path('', index_view, name='index'),
    path('add_file/', add_file_view, name='add_file'),
    path('add_directory/', add_directory_view, name='add_directory'),
    # path('show_file/<str:name>/', show_file_view, name='show_file'),
    # path('delete/', delete_view, name='delete'),
    # path('delete_file/', delete_file, name='delete_file'),
    # path('delete_directory/', delete_directory, name='delete_directory'),
    path('show_tab/<str:tab>/', show_tab, name='show_tab'),
    path('save_prover/', save_prover, name='save_prover'),
    path('save_vcs/', save_vcs, name='save_vcs'),
    # path('compile/', compile, name='compile'),
    path('js/show_file/', js_show_file, name='js_show_file'),
    path('js/delete_file/', js_delete_file, name='js_delete_file'),
    path('js/delete_directory/', js_delete_directory, name='js_delete_directory'),
    path('js/compile/', js_compile, name='js_compile'),
]