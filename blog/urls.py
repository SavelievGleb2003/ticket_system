from django.urls import path, re_path
from . import views

# create urls

urlpatterns = [
        path("", views.folder_list, name="folder_list"),
        path('my-documents/', views.user_documents_and_folders, name='user_documents_and_folders'),
        path('my-department/', views.documents_by_department, name='documents_by_department'),
        path("<int:folder_id>/", views.folder_list, name="folder_detail"),
        re_path(
                r'^TD/tag/(?P<tag_slug>[\w-]+)/$', views.ListTD.as_view(), name='TD_list_by_tag'
        ),
        path('folders/create/', views.create_folder, name='create_folder'),
        path('folders/<int:pk>/edit/', views.folder_update, name='folder_update'),
        path('folders/<int:pk>/delete/', views.folder_delete, name='folder_delete'),
        path('documents/create/', views.document_create, name='document_create'),
        path('documents/<int:pk>/edit/', views.document_update, name='document_update'),
        path('documents/<int:pk>/delete/', views.document_delete, name='document_delete'),
        path('<int:year>/<int:month>/<int:day>/<slug:TD>/', views.TD_detail, name='TD_detail'),
        path('<int:id_d>/share/',views.send_email, name='send_email'),
        path('<int:id_d>/comment/',views.add_comment, name='add_comment'),

]