import os

from django import template
from django.conf import settings
from dealer.git import git

register = template.Library()

@register.simple_tag
def revision(prod=False):
    _hrev = os.environ.get('HEROKU_SLUG_COMMIT', 'unknown')[:7]
    rev = git.revision if git.revision else _hrev
    if settings.DEBUG or settings.STAGING:
      channel = 'staging' if settings.STAGING else 'dev'
      return '#%s @%s' % (rev, channel)
    elif prod:
      return _hrev
    else:
      return ''
