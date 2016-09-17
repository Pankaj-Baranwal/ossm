import os

from django import template
from django.conf import settings
from dealer.git import git

register = template.Library()

@register.simple_tag
def revision():
    if settings.DEBUG or settings.STAGING:
      rev = git.revision if git.revision else os.environ.get('HEROKU_SLUG_COMMIT', 'unknown')[:7]
      channel = 'staging' if settings.STAGING else 'dev'
      return '#%s @%s' % (git.revision, channel)
    else:
      return ''
