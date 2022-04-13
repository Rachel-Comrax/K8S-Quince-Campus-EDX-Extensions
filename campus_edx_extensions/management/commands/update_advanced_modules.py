from django.core.management.base import BaseCommand
from openedx.core.djangoapps.content.course_overviews.models import \
    CourseOverview
from xmodule.modulestore.django import modulestore


class Command(BaseCommand):
    """
    Command to prefill or update edxnotes for existing courses
    """

    def handle(self, *args, **options):
        courses = CourseOverview.get_all_courses()
        course_keys = [course.id for course in courses]

        key_values = {"edxnotes": False, "edxnotes_visibility": False}

        for course in course_keys:
            with modulestore().bulk_operations(course):
                print(
                    f'================Start updating course "{str(course)}"================'
                )
                course_module = modulestore().get_course(course, depth=0)

                for key, value in key_values.items():
                    if hasattr(course_module, key):

                        try:
                            setattr(course_module, key, value)
                            modulestore().update_item(course_module, None)
                            print(
                                f'================Course "{str(course)}" advanced modules '
                                f"successfully updated================"
                            )
                        except AttributeError:
                            print(
                                f'================Something went wrong with course "{str(course)}"================'
                            )
                            continue
                    else:
                        print(
                            f'================Course "{str(course)}" has no have "{key}" attribute================'
                        )
