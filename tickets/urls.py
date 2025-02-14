from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('create/', views.create_ticket, name='create_ticket'),
]
