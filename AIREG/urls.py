from django.urls import path
from AIREG import views

urlpatterns = [
    path("", views.ai_regulations, name='ai_regulations'),
]
