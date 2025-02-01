from django.contrib import admin

from .models import TurnoverDocument, document_types
# Register your models here.



@admin.register(document_types)
class document_typesAdmin(admin.ModelAdmin):
    list_display = ['description']



@admin.register(TurnoverDocument)
class TurnoverDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','description', 'department', 'publish_by',
                    'document_type','document_file',
                    'filename', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'publish_by', 'auther', 'updated_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['auther']
    date_hierarchy = 'publish_by'
    ordering = ['status', 'publish_by', 'updated_at']
    show_facets = admin.ShowFacets.ALWAYS

    