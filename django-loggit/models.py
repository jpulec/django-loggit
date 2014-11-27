# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.template.context import Context
from django.template.loader import get_template_from_string
from django.utils import timezone
import swapper

from chewse.logsauce.context import actor_context_manager


class BaseLogEntry(models.Model):
    """
    A base class that implements the interface necessary to log an event.
    The render method returns a representation of this event.
    """
    event = models.ForeignKey(swapper.get_model_name('logsauce', 'LogEvent'),
        related_name='(classname)%s')
    created_ts = models.DateTimeField(default=timezone.now)

    def render(self, **kwargs):
        """
        A method to render this entry. This can be overridden to provide custom
        behavior. For example, if you want the entry to return a different
        rendering based on who was viewing it, or when it is being viewed.
        This default rendering just returns the event's rendering.
        """
        return self.event.render(self, **kwargs)
    render.allow_tags = True

    class Meta:
        abstract = True


class ActorLogEntryManager(models.Manager):
    """
    Custom model manager for AppLogEntry so we can check if None was explictly
    passed as a kwarg for creation.
    """
    def create(self, **kwargs):
        if not 'actor' in kwargs:
            kwargs['actor'] = actor_context_manager.actor
        return super(ActorLogEntryManager, self).create(**kwargs)


class ActorLogEntry(BaseLogEntry):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name="(classname)%s")

    objects = ActorLogEntryManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return "{0} performed event: {1}".format(unicode(self.actor),
            unicode(self.event))


class LogEntry(ActorLogEntry):
    class Meta(ActorLogEntry.Meta):
        swappable = swapper.swappable_setting('logsauce', 'LogEntry')


class BaseLogEvent(models.Model):
    """
    The base class that defines some event happening.
    """
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def get_context(self, **kwargs):
        return Context(kwargs)

    def render(self, entry, **kwargs):
        """
        Render method for a log event. This base method just returns the name.
        """
        return unicode(self.name)


class TemplateLogEvent(BaseLogEvent):
    """
    A subclass of BaseLogEvent that renders a template using django's
    templating engine. The current entry is added to the context that is passed
    to the template.
    """
    template = models.TextField()

    class Meta:
        abstract = True

    def render(self, entry, **kwargs):
        kwargs['entry'] = entry
        print kwargs['entry']
        context = self.get_context(**kwargs)
        return get_template_from_string(self.template).render(context)


class LogEvent(TemplateLogEvent):
    class Meta(TemplateLogEvent.Meta):
        swappable = swapper.swappable_setting('logsauce', 'LogEvent')
