from setting.views import log_view
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Notification, PushoverSetting, SystemMailSetting, Log, SlackSetting, TelegramSetting


class SystemMailSettingResource(resources.ModelResource):
    class Meta:
        model = SystemMailSetting
        skip_unchanged = True
        report_skipped = True


@admin.register(SystemMailSetting)
class SystemMailSettingAdmin(ImportExportModelAdmin):
    resource_class = SystemMailSettingResource

    list_display = [
        'mail_server', 'mail_port', 'mail_username', 'mail_sender',
        'mail_password'
    ]

    list_editable = ('mail_server', 'mail_port', 'mail_username',
                     'mail_sender', 'mail_password')

    list_display_links = None
    actions_on_top = True


class PushoverSettingResource(resources.ModelResource):
    class Meta:
        model = PushoverSetting
        skip_unchanged = True
        report_skipped = True


@admin.register(PushoverSetting)
class PushoverSettingAdmin(ImportExportModelAdmin):
    resource_class = PushoverSettingResource

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


class NotificatioResource(resources.ModelResource):
    class Meta:
        model = Notification
        import_id_fields = ('name', )
        exclude = ('id', )
        skip_unchanged = True
        report_skipped = True


@admin.register(Notification)
class NotificationAdmin(ImportExportModelAdmin):
    resource_class = NotificatioResource

    list_display = ['name', 'type', 'content']
    list_editable = ('name', 'type', 'content')

    list_display_links = None
    actions_on_top = True


@admin.register(Log)
class FeedbackStatsAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_content=None):
        return log_view(request)


class SlackSettingResource(resources.ModelResource):
    class Meta:
        model = PushoverSetting
        skip_unchanged = True
        report_skipped = True


@admin.register(SlackSetting)
class SlackSettingAdmin(admin.ModelAdmin):
    resource_class = SlackSettingResource

    list_display = ['token']
    list_editable = ('token', )

    list_display_links = None


class TelegramSettingResource(resources.ModelResource):
    class Meta:
        model = TelegramSetting
        skip_unchanged = True
        report_skipped = True


@admin.register(TelegramSetting)
class TelegramSettingAdmin(admin.ModelAdmin):
    resource_class = TelegramSettingResource

    list_display = ['token']
    list_editable = ('token', )

    list_display_links = None
