from django.urls import path
from . import views

# Create your views here.
urlpatterns = [
    path('split-text/', views.split_text_by_tokens, name='split_text'),
    path('split-text/output', views.split_output_files, name='split_output_files'),
]