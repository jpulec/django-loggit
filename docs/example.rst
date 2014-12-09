Example
=======

Models
------

To begin, just subclass the provided models, add your own fields, and override
any necessary methods.

A sample of how you may choose to setup your logging models:

.. code-block:: python

    from django.db import models

    from loggit.models import ActorMixin, BaseLogEntry, TemplateLogEvent


    class MyAppLogEntry(ActorMixin, BaseLogEntry):
        # Add any relevant extra fields you need for your application
        order = models.ForeignKey('orderapp.OrderModel')
        customer = models.ForeignKey('customerapp.CustomerModel')
        ...

        def save(self, **kwargs):
            # Do some other customer specific stuff here based on MyAppLogEvent
            # type
            return super(MyAppLogEntry, self).save(**kwargs)

    class MyAppLogEvent(TemplateLogEvent):
        # Add descriptions to my events
        description = models.TextField()

        def get_context(self, **kwargs):
          context = super(MyAppLogEvent, self).get_context(**kwargs)
          # Always add the url when rendering
          context['description'] = self.description
          return context


Or, using the mixins that incorporate the one to generic many relationship:

.. code-block:: python

    from operator import attrgetter

    from django.db import models

    from loggit.models import BaseLogEntry, M2MLogEntryMixin, M2MLogEventMixin, \
        TemplateLogEvent


    class MyAppLogEntry(M2MLogEntryMixin, BaseLogEntry):
        order_field = models.IntegerField()

    class MyAppLogEvent(M2MLogEventMixin, TemplateLogEvent):
        def get_context(self, **kwargs):
          # Save the entry for later use
          entry = kwargs.pop('entry')
          context = super(MyAppLogEvent, self).get_context(entry=entry, **kwargs)
          # For each list of models in the context, sort the list using the
          # field on the model named by entry.order_field
          context = {
            key: sorted(models, key=attrgetter(entry.order_field))
            for key, models in context
          }
          return context
