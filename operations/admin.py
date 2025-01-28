from django.contrib import admin
from .models import ProjectsModel, TransactionModel

@admin.register(ProjectsModel)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'started_at']
    list_display_links = ['name', 'type'] 
    search_fields = ['name', 'type'] 
    list_filter = ['name', 'type', 'started_at']


@admin.register(TransactionModel)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['sender__phone_number', 'receiver__phone_number', 'transaction_date']
    list_display_links = ['sender__phone_number'] 
    search_fields = ['sender__phone_number', 'receiver__phone_number'] 
    list_filter = ['transaction_date', 'status']