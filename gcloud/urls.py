from django.urls import path
from . import views

# Create your views here.
urlpatterns = [
    path('document-ai/', views.document_ai, name='document_ai'),
    path('document-ai/output/', views.doc_ai_output_view, name='doc_ai_output_view'),
    path('document-ai/ask-question/', views.ask_question_view, name='ask_question'),
]