# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.template.context import Context
from django.template.loader import get_template_from_string
from django.utils import timezone
import swapper


class BaseLogEntry(models.Model):
    """
    A base class that implements the interface necessary to log an event.
    The render method returns a representation of this event.
    """
    event = models.ForeignKey(swapper.get_model_name('loggit', 'LogEvent'),
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

    class Meta:
        abstract = True


class ActorMixin(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name="(classname)%s")

    class Meta:
        abstract = True


class LogEntry(BaseLogEntry, ActorMixin):
    class Meta(BaseLogEntry.Meta):
        swappable = swapper.swappable_setting('loggit', 'LogEntry')


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
        context = self.get_context(**kwargs)
        return get_template_from_string(self.template).render(context)


class LogEvent(TemplateLogEvent):
    class Meta(TemplateLogEvent.Meta):
        swappable = swapper.swappable_setting('loggit', 'LogEvent')


# Optional models using django-genericm2m that allow attaching of objects to
# a log event
try:
    from collections import defaultdict
    from genericm2m.models import RelatedObjectsDescriptor
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType

    class RelatedObject(models.Model):
        log_entry = models.ForeignKey(swapper.get_model_name('loggit', 'LogEntry'),
            related_name='log_entries')

        # ACTUAL RELATED OBJECT:
        content_type = models.ForeignKey(ContentType, related_name="related_%(class)s")
        object_id = models.IntegerField(db_index=True)
        object = GenericForeignKey(fk_field="object_id")

        label = models.CharField(max_length=255)

    class M2MLogEntryMixin(models.Model):
        related = RelatedObjectsDescriptor(RelatedObject, 'log_entry', 'object')

        class Meta:
            abstract = True

    class M2MLogEventMixin(object):
        def get_context(self, **kwargs):
            entry = kwargs.pop('entry')
            models_context = defaultdict(list)
            for relation in entry.related.order_by('label'):
                models_context[relation.label].append(relation.object)
            return super(M2MLogEventMixin, self).get_context(**models_context)

except ImportError:
    pass
