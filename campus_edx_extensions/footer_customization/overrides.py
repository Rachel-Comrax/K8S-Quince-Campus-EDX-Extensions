import logging

from django.conf import settings
from django.urls import reverse, NoReverseMatch
from six.moves.urllib.parse import urljoin
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from edx_django_utils.monitoring import set_custom_attribute
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from xmodule.util.xmodule_django import get_current_request_hostname  # lint-amnesty, pylint: disable=wrong-import-order

log = logging.getLogger(__name__)

def marketing_link(base_func, name):
    """Returns the correct URL for a link to the marketing site
    depending on if the marketing site is enabled

    Since the marketing site is enabled by a setting, we have two
    possible URLs for certain links. This function is to decides
    which URL should be provided.
    """
    # link_map maps URLs from the marketing site to the old equivalent on
    # the Django site
    link_map = settings.MKTG_URL_LINK_MAP
    enable_mktg_site = configuration_helpers.get_value(
        'ENABLE_MKTG_SITE',
        settings.FEATURES.get('ENABLE_MKTG_SITE', False)
    )
    enable_custom_mktg_site = configuration_helpers.get_value(
        'ENABLE_MKTG_CUSTOM_SITE',
        settings.FEATURES.get('ENABLE_MKTG_CUSTOM_SITE', False)
    )
    marketing_url_overrides = configuration_helpers.get_value(
        'MKTG_URL_OVERRIDES',
        settings.MKTG_URL_OVERRIDES
    )
    
    # get the marketing site URLs dictionary
    marketing_urls = {}
    if enable_mktg_site:
        marketing_urls = configuration_helpers.get_value(
            'MKTG_URLS',
            settings.MKTG_URLS
        )
    elif enable_custom_mktg_site:
        marketing_urls = configuration_helpers.get_value(
            'MKTG_CUSTOM_URLS',
            settings.MKTG_CUSTOM_URLS
        )

    if name in marketing_url_overrides:
        validate = URLValidator()
        url = marketing_url_overrides.get(name)
        try:
            validate(url)
            return url
        except ValidationError as err:
            log.debug("Invalid link set for link %s: %s", name, err)
            return '#'

    if (enable_mktg_site or enable_custom_mktg_site) and name in marketing_urls:
        # special case for when we only want the root marketing URL
        if name == 'ROOT':
            return marketing_urls.get('ROOT')
        # special case for new enterprise marketing url with custom tracking query params
        if name == 'ENTERPRISE':
            enterprise_url = marketing_urls.get(name)
            # if url is not relative, then return it without joining to root
            if not enterprise_url.startswith('/'):
                return enterprise_url
        # Using urljoin here allows us to enable a marketing site and set
        # a site ROOT, but still specify absolute URLs for other marketing
        # URLs in the MKTG_URLS setting
        # e.g. urljoin('https://marketing.com', 'https://open-edx.org/about') >>> 'https://open-edx.org/about'
        return urljoin(marketing_urls.get('ROOT'), marketing_urls.get(name))
    # only link to the old pages when the marketing site isn't on
    elif not (enable_mktg_site or enable_custom_mktg_site) and name in link_map:
        # don't try to reverse disabled marketing links
        if link_map[name] is not None:
            host_name = get_current_request_hostname()  # lint-amnesty, pylint: disable=unused-variable
            if link_map[name].startswith('http'):
                return link_map[name]
            else:
                try:
                    return reverse(link_map[name])
                except NoReverseMatch:
                    log.debug("Cannot find corresponding link for name: %s", name)
                    set_custom_attribute('unresolved_marketing_link', name)
                    return '#'
    else:
        log.debug("Cannot find corresponding link for name: %s", name)
        return '#'
    
def is_marketing_link_set(name):
    """
    Returns a boolean if a given named marketing link is configured.
    """

    enable_mktg_site = configuration_helpers.get_value(
        'ENABLE_MKTG_SITE',
        settings.FEATURES.get('ENABLE_MKTG_SITE', False)
    )
    marketing_urls = configuration_helpers.get_value(
        'MKTG_URLS',
        settings.MKTG_URLS
    )

    if enable_mktg_site:
        return name in marketing_urls
    else:
        return name in settings.MKTG_URL_LINK_MAP
