from django.contrib import admin

from .models import TurnoverDocument, document_types, Comment
# Register your models here.



@admin.register(document_types)
class document_typesAdmin(admin.ModelAdmin):
    list_display = ['description']



@admin.register(TurnoverDocument)
class TurnoverDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','description', 'department', 'publish_by',
                    'document_type','document_file',
                    'filename', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'publish_by', 'author', 'updated_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish_by'
    ordering = ['status', 'publish_by', 'updated_at']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'description', 'document',
                    'created_at', 'updated_at', 'active']
    list_filter = ['active','created_at', 'updated_at', ]
    search_fields = ['name', 'description']
    ordering = ['name', 'email', 'description']
