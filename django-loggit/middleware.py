# -*- coding: utf-8 -*-

from chewse.logsauce.context import actor_context_manager


class ActorMiddleware(object):
    """
    Wrap a request with a context that contains the current request.user
    as the actor for any actions.
    This is similar to how django-reversion does it.
    """
    def process_request(self, request):
        """
        Check to see that the session exists and that a user is on
        the request and then set them to the actor on actor_context_manager.
        """
        if hasattr(request, 'session') and hasattr(request, "user"):
            if request.user.is_authenticated():
                actor_context_manager.actor = request.user
            else:
                actor_context_manager.actor = None
