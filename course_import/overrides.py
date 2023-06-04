"""
Campus course import overrides.
"""
import base64
import logging
import os
import re
import shutil

from django.conf import settings
from django.core.files import File
from django.utils.translation import ugettext as _
from path import Path as path
from six import text_type

from common.djangoapps.util.json_request import JsonResponse


log = logging.getLogger(__name__)

# Regex to capture Content-Range header ranges.
CONTENT_RE = re.compile(r"(?P<start>\d{1,11})-(?P<stop>\d{1,11})/(?P<end>\d{1,11})")


def write_chunk_override(prev_fn, request, courselike_key):
    """
    Write the OLX file data chunk from the given request to the local filesystem.
    """
    from cms.djangoapps.contentstore.storage import course_import_export_storage
    from cms.djangoapps.contentstore.tasks import import_olx
    from cms.djangoapps.contentstore.views.import_export import _save_request_status
    from cms.djangoapps.contentstore.utils import reverse_course_url

    # Upload .tar.gz to local filesystem for one-server installations not using S3 or Swift
    data_root = path(settings.GITHUB_REPO_ROOT)
    subdir = base64.urlsafe_b64encode(repr(courselike_key).encode('utf-8')).decode('utf-8')
    course_dir = data_root / subdir
    filename = request.FILES['course-data'].name

    courselike_string = text_type(courselike_key) + filename
    # Do everything in a try-except block to make sure everything is properly cleaned up.
    try:
        # Use sessions to keep info about import progress
        _save_request_status(request, courselike_string, 0)

        if not filename.endswith('.tar.gz'):
            _save_request_status(request, courselike_string, -1)
            return JsonResponse(
                {
                    'ErrMsg': _('We only support uploading a .tar.gz file.'),
                    'Stage': -1
                },
                status=415
            )

        temp_filepath = course_dir / filename
        if not course_dir.isdir():
            os.mkdir(course_dir)

        logging.debug(u'importing course to {0}'.format(temp_filepath))

        # Get upload chunks byte ranges
        try:
            matches = CONTENT_RE.search(request.META["HTTP_CONTENT_RANGE"])
            content_range = matches.groupdict()
        except KeyError:  # Single chunk
            # no Content-Range header, so make one that will work
            content_range = {'start': 0, 'stop': 1, 'end': 2}

        # stream out the uploaded files in chunks to disk
        if int(content_range['start']) == 0:
            mode = "wb+"
        else:
            FILE_READ_CHUNK = 1024  # bytes
            archive_path = 'olx_import/' + filename

            # Copy the OLX archive from where it was uploaded to (S3, Swift, file system, etc.)
            if not course_import_export_storage.exists(archive_path):
                log.info(u'Course import %s: Uploaded file %s not found', courselike_key, archive_path)
                return
            with course_import_export_storage.open(archive_path, 'rb') as source:
                with open(temp_filepath, 'wb') as destination:
                    def read_chunk():
                        """
                        Read and return a sequence of bytes from the source file.
                        """
                        return source.read(FILE_READ_CHUNK)
                    for chunk in iter(read_chunk, b''):
                        destination.write(chunk)
            log.info(u'Course import %s: Download from storage complete', courselike_key)
            # Delete from source location
            course_import_export_storage.delete(archive_path)

            mode = "ab+"
            size = os.path.getsize(temp_filepath)
            # Check to make sure we haven't missed a chunk
            # This shouldn't happen, even if different instances are handling
            # the same session, but it's always better to catch errors earlier.
            if size < int(content_range['start']):
                _save_request_status(request, courselike_string, -1)
                log.warning(
                    u"Reported range %s does not match size downloaded so far %s",
                    content_range['start'],
                    size
                )
                return JsonResponse(
                    {
                        'ErrMsg': _('File upload corrupted. Please try again'),
                        'Stage': -1
                    },
                    status=409
                )
            # The last request sometimes comes twice. This happens because
            # nginx sends a 499 error code when the response takes too long.
            elif size > int(content_range['stop']) and size == int(content_range['end']):
                return JsonResponse({'ImportStatus': 1})

        with open(temp_filepath, mode) as temp_file:  # pylint: disable=W6005
            for chunk in request.FILES['course-data'].chunks():
                temp_file.write(chunk)

        size = os.path.getsize(temp_filepath)

        if int(content_range['stop']) != int(content_range['end']) - 1:
            with open(temp_filepath, 'rb') as local_file:  # pylint: disable=W6005
                django_file = File(local_file)
                storage_path = course_import_export_storage.save(u'olx_import/' + filename, django_file)
            # More chunks coming
            return JsonResponse({
                "files": [{
                    "name": filename,
                    "size": size,
                    "deleteUrl": "",
                    "deleteType": "",
                    "url": reverse_course_url('import_handler', courselike_key),
                    "thumbnailUrl": ""
                }]
            })

        log.info(u"Course import %s: Upload complete", courselike_key)
        with open(temp_filepath, 'rb') as local_file:  # pylint: disable=W6005
            django_file = File(local_file)
            storage_path = course_import_export_storage.save(u'olx_import/' + filename, django_file)
        import_olx.delay(
            request.user.id, text_type(courselike_key), storage_path, filename, request.LANGUAGE_CODE)

    # Send errors to client with stage at which error occurred.
    except Exception as exception:  # pylint: disable=broad-except
        _save_request_status(request, courselike_string, -1)
        if course_dir.isdir():
            shutil.rmtree(course_dir)
            log.info(u"Course import %s: Temp data cleared", courselike_key)

        log.exception(
            "error importing course"
        )
        return JsonResponse(
            {
                'ErrMsg': str(exception),
                'Stage': -1
            },
            status=400
        )

    return JsonResponse({'ImportStatus': 1})
