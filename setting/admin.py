from django.contrib import admin
from .models import SystemMailSetting, Notification, PushoverSetting


@admin.register(SystemMailSetting)
class SystemMailSettingAdmin(admin.ModelAdmin):
    list_display = [
        'mail_server', 'mail_port', 'mail_username', 'mail_sender',
        'mail_password'
    ]

    list_editable = ('mail_server', 'mail_port', 'mail_username',
                     'mail_sender', 'mail_password')

    list_display_links = None
    actions_on_top = True


@admin.register(PushoverSetting)
class PushoverSettingAdmin(admin.ModelAdmin):
    list_display = ['api_token']
    list_editable = ('api_token', )

    list_display_links = None
    actions_on_top = True

    actions = ['custom_button']

    def custom_button(self, request, queryset):
        pass

    custom_button.short_description = '新建Pushover Application'
    custom_button.type = 'info'
    custom_button.action_type = 2
    custom_button.action_url = 'https://pushover.net/'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'content']

    list_editable = ('name', 'type', 'content')

    list_display_links = None
    actions_on_top = True
