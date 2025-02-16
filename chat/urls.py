from django.urls import path, re_path
from . import views

# create urls

urlpatterns = [
    path('<int:ticket_id>/', views.chat_detail, name='chat_detail'),
    path('send_message/<int:chat_id>/', views.send_message, name='send_message'),
]