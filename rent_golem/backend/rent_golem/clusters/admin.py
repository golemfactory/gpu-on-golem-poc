from django.contrib import admin

from clusters.models import Cluster, Worker

class ClusterAdmin(admin.ModelAdmin):
    class WorkerInline(admin.StackedInline):
        model = Worker
        extra = 0
        max_num = 0
        can_delete = False
        readonly_fields = ('provider', 'service_id', 'address', 'status', 'created_at', 'last_update')

    inlines = [WorkerInline]


admin.site.register(Cluster, ClusterAdmin)
