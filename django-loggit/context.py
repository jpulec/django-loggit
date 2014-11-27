# -*- coding: utf-8 -*-

from threading import local


class ActorContextManager(local):
    """
    This just holds onto the current actor based. This will be set by middleware
    to be request.user. This subclasses local to have different data for each
    thread.
    """
    def __init__(self):
        """
        Just clear whatever is set to the actor.
        """
        self.actor = None


# A shared, thread-safe context manager.
actor_context_manager = ActorContextManager()
