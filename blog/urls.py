from django.urls import path, re_path
from . import views

# create urls

urlpatterns = [
        path("", views.folder_list, name="folder_list"),
        path('my-documents/', views.user_documents_and_folders, name='user_documents_and_folders'),
        path('my-department/', views.documents_by_department, name='documents_by_department'),
        path("<int:parent_id>/", views.folder_list, name="folder_detail"),
        re_path(
                r'^TD/tag/(?P<tag_slug>[\w-]+)/$', views.ListTD.as_view(), name='TD_list_by_tag'
        ),
        path('<int:year>/<int:month>/<int:day>/<slug:TD>/', views.TD_detail, name='TD_detail'),
        path('<int:id_d>/share/',views.send_email, name='send_email'),
        path('<int:id_d>/comment/',views.add_comment, name='add_comment'),

]