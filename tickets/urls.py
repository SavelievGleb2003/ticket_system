from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('ticket_list_created_by', views.ticket_list_created_by, name='ticket_list_created_by'),
    path('ticket_list_accepted_by', views.ticket_list_accepted_by, name='ticket_list_accepted_by'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('accept_ticket/<int:ticket_id>/', views.accept_ticket, name='accept_ticket'),
    path('close_ticket/<int:ticket_id>/', views.close_ticket, name='close_ticket'),
    path('create/', views.create_ticket, name='create_ticket'),
]
