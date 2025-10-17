from django.urls import path
from . import views

app_name = 'buses'

urlpatterns = [
    path('schedule/', views.add_schedule_view, name='schedule'),
]
