from django.urls import path
from . import views

urlpatterns = [
    path('rate/<int:teacher_id>/', views.rate_teacher, name='rate_teacher'),
    # Temporarily removed: path('observer-demo/', views.observer_demo, name='observer_demo'),
]
