Quick Start
===========

Install
-------

This package is available on `PyPI`_.

Install from PyPI with ``pip``:

.. code-block:: bash

    $ pip install django-loggit

.. _pypi: https://pypi.python.org/pypi/django-loggit/


Configure
---------

Settings
~~~~~~~~

Add ``loggit`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'loggit',
    ]

Django-loggit ships with a mixin to track whick user was responsible for a
``LogEntry`` being created. To enable this functionality you must add the
following to your middleware settings:

.. code-block:: python

    MIDDLEWARE_CLASSES = [
        # ...
        'loggit.middleware.ActorMiddleware',
    ]

Models
~~~~~~

Included with django-loggit are two base abstract classes, ``BaseLogEvent`` and
``BaseLogEntry``` and two concrete implementations of those base classes,
``LogEvent`` and ``LogEntry``, which are swappable models.

.. note::

    Although these two classes are provided, you are STRONGLY urged to subclass
    the base classes and implment models in your app. Since these are swappable
    models, you MUST not swap them for the lifetime of your migrations.
    Therefore, it is very beneficial to be able to alter a model that exists in
    your own app. As a caveat to migrations, your model MUST belong to the first
    migration of the app it belogns to. Read more about swappable models here:
    `Django Migration Dependencies`_ and `Django Customizing User Auth`_.

.. _django migration dependencies: https://docs.djangoproject.com/en/dev/topics/migrations/#dependencies
.. _django customizing user auth: https://docs.djangoproject.com/en/dev/topics/auth/customizing/#substituting-a-custom-user-model


A few mixins are also provided to help you compose your models. The
``TemplateLogEvent`` mixin provides template rendering via django's template
engine and retrieve's a context via the overrideable ``get_context()`` method
in a similar fashion to how django's Class Based Generic Views work. Another
mixin is the ``ActorMixin`` which when used with the provided middleware will
log what user was responsible for an entry being created using the current
request.


Optionals
---------

You may optionally choose to install `django-generic-m2m`_ to be used in
conjunction with django-loggit. Two mixins ship with django-loggit, and a
third model for tracking the relationships between an event and any sets of
objects via generics. The ``M2MLogEntry`` mixin just adds the descriptor for
a one way relationships to any type of object, as described in the Model
``RelatedObject``. The ``M2MLogEventMixin`` simply overrides the
``get_context()`` method for an event to coalesce all of the objects under
the same label and return them as a dictionary.


.. _django-generic-m2m: https://github.com/coleifer/django-generic-m2m
