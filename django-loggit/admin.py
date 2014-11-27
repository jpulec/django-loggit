# -*- coding: utf-8 -*-

from django.contrib import admin

from chewse.logsauce.models import LogEntry, LogEvent


class LogEntryAdmin(admin.ModelAdmin):
    fields = ['event', 'actor', 'created_ts', 'render',]
    readonly_fields = ['render',]


admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(LogEvent)
