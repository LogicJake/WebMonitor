import logging

from django.contrib import admin, messages
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from task.models import Content, RSSTask, Task, TaskStatus
from task.utils.scheduler import remove_job

logger = logging.getLogger('admin')


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = [
        'task_name', 'last_run', 'short_last_status', 'task_status',
        'task_type'
    ]
    list_editable = ['task_status']
    list_per_page = 10
    list_display_links = None

    actions_on_top = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class TaskResource(resources.ModelResource):
    class Meta:
        model = Task
        import_id_fields = ('name', )
        exclude = ('id', )
        skip_unchanged = True
        report_skipped = True


@admin.register(Task)
class TaskAdmin(ImportExportModelAdmin):
    resource_class = TaskResource

    list_display = [
        'id', 'name', 'url', 'frequency', 'selector', 'create_time',
        'is_chrome', 'regular_expression', 'rule', 'headers'
    ]
    list_editable = ('name', 'url', 'frequency', 'is_chrome',
                     'regular_expression', 'rule', 'headers', 'selector')
    filter_horizontal = ('notification', )

    list_per_page = 10

    def has_delete_permission(self, request, obj=None):
        return False

    def redefine_delete_selected(self, request, obj):
        for o in obj.all():
            id = o.id
            remove_job(id)

            TaskStatus.objects.filter(task_id=id, task_type='html').delete()
            Content.objects.filter(task_id=id, task_type='html').delete()

            o.delete()
            logger.info('task_{}删除'.format(id))

        messages.add_message(request, messages.SUCCESS, '删除成功')

    redefine_delete_selected.short_description = '删除'
    redefine_delete_selected.icon = 'el-icon-delete'
    redefine_delete_selected.style = 'color:white;background:red'

    actions = ['redefine_delete_selected']


class RSSTaskResource(resources.ModelResource):
    class Meta:
        model = RSSTask
        import_id_fields = ('name', )
        exclude = ('id', )
        skip_unchanged = True
        report_skipped = True


@admin.register(RSSTask)
class RSSTaskAdmin(ImportExportModelAdmin):
    resource_class = RSSTaskResource

    list_display = ['id', 'name', 'url', 'frequency', 'create_time']
    list_editable = ('name', 'url', 'frequency')
    filter_horizontal = ('notification', )

    list_per_page = 10

    def has_delete_permission(self, request, obj=None):
        return False

    def redefine_delete_selected(self, request, obj):
        for o in obj.all():
            id = o.id
            remove_job(id, 'rss')

            TaskStatus.objects.filter(task_id=id, task_type='rss').delete()
            Content.objects.filter(task_id=id, task_type='rss').delete()

            o.delete()
            logger.info('task_RSS{}删除'.format(id))

        messages.add_message(request, messages.SUCCESS, '删除成功')

    redefine_delete_selected.short_description = '删除'
    redefine_delete_selected.icon = 'el-icon-delete'
    redefine_delete_selected.style = 'color:white;background:red'

    actions = ['redefine_delete_selected']
