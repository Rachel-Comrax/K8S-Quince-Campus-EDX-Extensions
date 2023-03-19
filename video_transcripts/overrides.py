"""
Utility methods for Enterprise
"""

import json
import logging

import six
from django.core.files.base import ContentFile

from edxval.api import create_external_video, create_or_update_video_transcript, delete_video_transcript
from webob import Response
from xmodule.exceptions import NotFoundError

from common.lib.xmodule.xmodule.video_module.transcripts_utils import (
    Transcript,
    TranscriptsGenerationException,
    clean_video_id,
    get_transcript,
)

log = logging.getLogger(__name__)

def studio_transcript(prev_fn, self, request, dispatch):
        """
        Entry point for Studio transcript handlers.

        Dispatches:
            /translation/[language_id] - language_id sould be in url.

        `translation` dispatch support following HTTP methods:
            `POST`:
                Upload srt file. Check possibility of generation of proper sjson files.
                For now, it works only for self.transcripts, not for `en`.
                Do not update self.transcripts, as fields are updated on save in Studio.
            `GET:
                Return filename from storage. SRT format is sent back on success. Filename should be in GET dict.

        We raise all exceptions right in Studio:
            NotFoundError:
                Video or asset was deleted from module/contentstore, but request came later.
                Seems impossible to be raised. module_render.py catches NotFoundErrors from here.

            /translation POST:
                TypeError:
                    Unjsonable filename or content.
                TranscriptsGenerationException, TranscriptException:
                    no SRT extension or not parse-able by PySRT
                UnicodeDecodeError: non-UTF8 uploaded file content encoding.
        """
        _ = self.runtime.service(self, "i18n").ugettext

        if dispatch.startswith('translation'):

            if request.method == 'POST':
                error = self.validate_transcript_upload_data(data=request.POST)
                if error:
                    response = Response(json={'error': error}, status=400)
                else:
                    edx_video_id = clean_video_id(request.POST['edx_video_id'])
                    language_code = request.POST['language_code']
                    new_language_code = request.POST['new_language_code']
                    transcript_file = request.POST['file'].file

                    if not edx_video_id:
                        # Back-populate the video ID for an external video.
                        # pylint: disable=attribute-defined-outside-init
                        self.edx_video_id = edx_video_id = create_external_video(display_name=u'external video')

                    try:
                        # Convert SRT transcript into an SJSON format
                        # and upload it to S3.
                        sjson_subs = Transcript.convert(
                            content=transcript_file.read().decode('utf-8'),
                            input_format=Transcript.SRT,
                            output_format=Transcript.SJSON
                        ).encode()
                        create_or_update_video_transcript(
                            video_id=edx_video_id,
                            language_code=language_code,
                            metadata={
                                'file_format': Transcript.SJSON,
                                'language_code': new_language_code
                            },
                            file_data=ContentFile(sjson_subs),
                        )
                        payload = {
                            'edx_video_id': edx_video_id,
                            'language_code': new_language_code
                        }
                        response = Response(json.dumps(payload), status=201)
                    except (TranscriptsGenerationException, UnicodeDecodeError):
                        response = Response(
                            json={
                                'error': _(
                                    u'There is a problem with this transcript file. Try to upload a different file.'
                                )
                            },
                            status=400
                        )
            elif request.method == 'DELETE':
                # // delete request.method == 'DELETE' function - the user won't be able to delete the transcript anymore
                log.warning(f"Someone tried to delete video-transcripts from his course, data of request (request.method == 'DELETE') - {request}")
                return Response(status=200)
                # request_data = request.json

                # if 'lang' not in request_data or 'edx_video_id' not in request_data:
                #     return Response(status=400)

                # language = request_data['lang']
                # edx_video_id = clean_video_id(request_data['edx_video_id'])

                # if edx_video_id:
                #     delete_video_transcript(video_id=edx_video_id, language_code=language)

                # if language == u'en':
                #     # remove any transcript file from content store for the video ids
                #     possible_sub_ids = [
                #         self.sub,  # pylint: disable=access-member-before-definition
                #         self.youtube_id_1_0
                #     ] + get_html5_ids(self.html5_sources)
                #     for sub_id in possible_sub_ids:
                #         remove_subs_from_store(sub_id, self, language)

                #     # update metadata as `en` can also be present in `transcripts` field
                #     remove_subs_from_store(self.transcripts.pop(language, None), self, language)

                #     # also empty `sub` field
                #     self.sub = ''  # pylint: disable=attribute-defined-outside-init
                # else:
                #     remove_subs_from_store(self.transcripts.pop(language, None), self, language)

                # return Response(status=200)

            elif request.method == 'GET':
                language = request.GET.get('language_code')
                if not language:
                    return Response(json={'error': _(u'Language is required.')}, status=400)

                try:
                    transcript_content, transcript_name, mime_type = get_transcript(
                        video=self, lang=language, output_format=Transcript.SRT
                    )
                    response = Response(transcript_content, headerlist=[
                        (
                            'Content-Disposition',
                            'attachment; filename="{}"'.format(
                                transcript_name.encode('utf8') if six.PY2 else transcript_name
                            )
                        ),
                        ('Content-Language', language),
                        ('Content-Type', mime_type)
                    ])
                except (UnicodeDecodeError, TranscriptsGenerationException, NotFoundError):
                    response = Response(status=404)

            else:
                # Any other HTTP method is not allowed.
                response = Response(status=404)

        else:  # unknown dispatch
            log.debug("Dispatch is not allowed")
            response = Response(status=404)

        return response
