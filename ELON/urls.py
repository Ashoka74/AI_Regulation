from django.urls import path
from ELON import views

urlpatterns = [
    path("", views.ai_regulations, name='ai_regulations'),
]
