from django.contrib import admin
from django.contrib.auth.models import Group

from app1.models import CustomUser, Reserve, Record, Openness

admin.site.site_title = "管理后台"
admin.site.site_header = "管理后台"
admin.site.index_title = "管理后台"
admin.site.unregister(Group)


# Register your models here.

@admin.register(CustomUser)
class AdminCustomUser(admin.ModelAdmin):
    list_display = [i.name for i in CustomUser._meta.fields]


@admin.register(Reserve)
class AdminReserve(admin.ModelAdmin):
    list_display = [i.name for i in Reserve._meta.fields]


@admin.register(Record)
class AdminRecord(admin.ModelAdmin):
    list_display = [i.name for i in Record._meta.fields]
    list_display.append('shi_')

    @admin.display(description='预约时间段', ordering='id')
    def shi_(self, obj):
        return '{}至{}'.format(obj.openness.start_time, obj.openness.end_time)


@admin.register(Openness)
class AdminOpenness(admin.ModelAdmin):
    list_display = [i.name for i in Openness._meta.fields]
