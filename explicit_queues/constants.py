from django.conf import settings


HIGH_MEM_QUEUE = getattr(settings, "HIGH_MEM_QUEUE", f'edx.{settings.QUEUE_VARIANT}core.high_mem')
LOW_PRIORITY_QUEUE = getattr(settings, "LOW_PRIORITY_QUEUE", f'edx.{settings.QUEUE_VARIANT}core.low')

INSTRUCTOR_TASK_ROUTING_KEY = HIGH_MEM_QUEUE

EVENTTRACKING_ROUTING_KEY = LOW_PRIORITY_QUEUE
COMPLETION_AGGREGATOR_ROUTING_KEY = LOW_PRIORITY_QUEUE
DIGITAL_GOV_REPORTS_ROUTING_KEY = LOW_PRIORITY_QUEUE

EXTENDED_EXPLICIT_QUEUES = {
    # high priority
    'lms.djangoapps.instructor_task.tasks.send_bulk_course_email': {
        'queue': settings.ACE_ROUTING_KEY},
    'openedx.core.djangoapps.user_authn.tasks.send_activation_email': {
        'queue': settings.ACE_ROUTING_KEY},
    'lms.djangoapps.discussion.tasks.send_ace_message': {
        'queue': settings.ACE_ROUTING_KEY},
    # high mem
    'lms.djangoapps.instructor_task.tasks.generate_anonymous_ids_for_course': {
        'queue': INSTRUCTOR_TASK_ROUTING_KEY},
    'lms.djangoapps.instructor_task.tasks.override_problem_score': {
        'queue': INSTRUCTOR_TASK_ROUTING_KEY},
    'lms.djangoapps.instructor_task.tasks.proctored_exam_results_csv': {
        'queue': INSTRUCTOR_TASK_ROUTING_KEY},
    'lms.djangoapps.instructor_task.tasks.reset_problem_attempts': {
        'queue': INSTRUCTOR_TASK_ROUTING_KEY},
    'lms.djangoapps.instructor_task.tasks.calculate_may_enroll_csv': {
        'queue': INSTRUCTOR_TASK_ROUTING_KEY},
    'lms.djangoapps.instructor_task.tasks.calculate_problem_responses_csv': {
        'queue': INSTRUCTOR_TASK_ROUTING_KEY},
    'lms.djangoapps.instructor_task.tasks.calculate_students_features_csv': {
        'queue': INSTRUCTOR_TASK_ROUTING_KEY},
    'lms.djangoapps.instructor_task.tasks.rescore_problem': {
        'queue': INSTRUCTOR_TASK_ROUTING_KEY},
    'lms.djangoapps.instructor_task.tasks.calculate_students_features_csv': {
        'queue': INSTRUCTOR_TASK_ROUTING_KEY},
    'lms.djangoapps.instructor_task.tasks.export_ora2_data': {
        'queue': INSTRUCTOR_TASK_ROUTING_KEY},
    'lms.djangoapps.instructor_task.tasks.export_ora2_submission_files': {
        'queue': INSTRUCTOR_TASK_ROUTING_KEY},
    'lms.djangoapps.instructor_task.tasks.export_ora2_summary': {
        'queue': INSTRUCTOR_TASK_ROUTING_KEY},
    # low
    'eventtracking.tasks.send_event': {
        'queue': EVENTTRACKING_ROUTING_KEY},
    'digital_gov_reports.courses_report.run_digital_data_to_report': {
        'queue': DIGITAL_GOV_REPORTS_ROUTING_KEY},
    'completion_aggregator.tasks.aggregation_tasks.update_aggregators': {
        'queue': COMPLETION_AGGREGATOR_ROUTING_KEY},
    'event_routing_backends.tasks.dispatch_event': {
        'queue': COMPLETION_AGGREGATOR_ROUTING_KEY},
    'event_routing_backends.tasks.dispatch_event_persistent': {
        'queue': COMPLETION_AGGREGATOR_ROUTING_KEY},
}
