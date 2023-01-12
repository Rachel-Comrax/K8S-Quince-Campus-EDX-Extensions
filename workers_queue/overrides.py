from common.djangoapps.util.db import outer_atomic
from lms.djangoapps.instructor_task.api_helper import _reserve_task, _get_xmodule_instance_args, _handle_instructor_task_failure

def submit_task(base_func, request, task_type, task_class, course_key, task_input, task_key):
    """
    Helper method to submit a task.

    Reserves the requested task, based on the `course_key`, `task_type`, and `task_key`,
    checking to see if the task is already running.  The `task_input` is also passed so that
    it can be stored in the resulting InstructorTask entry.  Arguments are extracted from
    the `request` provided by the originating server request.  Then the task is submitted to run
    asynchronously, using the specified `task_class` and using the task_id constructed for it.

    Cannot be inside an atomic block.

    `AlreadyRunningError` is raised if the task is already running.
    """
    with outer_atomic():
        # check to see if task is already running, and reserve it otherwise:
        instructor_task = _reserve_task(course_key, task_type, task_key, task_input, request.user)

    # make sure all data has been committed before handing off task to celery.

    task_id = instructor_task.task_id
    task_args = [instructor_task.id, _get_xmodule_instance_args(request, task_id)]
    try:
        queue = task_input.get('queue')
        if queue is None:
            task_class.apply_async(task_args, task_id=task_id)
        else: 
            task_class.apply_async(task_args, queue=queue, task_id=task_id)
            
    except Exception as error:
        _handle_instructor_task_failure(instructor_task, error)

    return instructor_task