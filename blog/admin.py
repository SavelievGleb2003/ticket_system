from django.contrib import admin

from .models import TurnoverDocument, document_types
# Register your models here.



@admin.register(document_types)
class document_typesAdmin(admin.ModelAdmin):
    list_display = ['description']



@admin.register(TurnoverDocument)
class TurnoverDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'department', 'publish',
                    'document_type','document_file',
                    'filename', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'publish', 'auther', 'updated_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['auther']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish', 'updated_at']
    show_facets = admin.ShowFacets.ALWAYS

    