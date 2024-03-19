from explicit_queues.constants import EXTENDED_EXPLICIT_QUEUES


def route_task(base_fn, name, args, kwargs, options, task=None, **kw):  # pylint: disable=unused-argument
    """
    Celery-defined method allowing for custom routing logic.

    If None is returned from this method, default routing logic is used.
    """
    if name in EXTENDED_EXPLICIT_QUEUES:
        return EXTENDED_EXPLICIT_QUEUES[name]

    return base_fn(name, args, kwargs, options, task=None, **kw)
