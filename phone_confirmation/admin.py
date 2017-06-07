from django.contrib import admin

from phone_confirmation.models import PhoneConfirmation


@admin.register(PhoneConfirmation)
class PhoneConfirmation(admin.ModelAdmin):
    list_display = ('created_at', 'phone_number', 'code')
    list_filter = ('created_at',)
    search_fields = ('phone_number',)
