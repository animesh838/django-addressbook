from django.contrib import admin
from .models import Contact

# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'city', 'state', 'created_at')
    list_filter = ('created_at', 'updated_at', 'city', 'state', 'country')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('first_name', 'last_name')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )
