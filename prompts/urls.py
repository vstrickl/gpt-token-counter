from django.urls import path
from . import views

# Create your views here.
urlpatterns = [
    path('count/', views.token_counter, name='count'),
    path('split/', views.split_file_by_tokens, name='split'),
    path('count/num-tokens', views.num_tokens, name='num_tokens'),
    path('split/output', views.split_output_files, name='split_output_files'),
    path('split/output/<filename>/', views.render_markdown_view, name='markdown_view'),
]