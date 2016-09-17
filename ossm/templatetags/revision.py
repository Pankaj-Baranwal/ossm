from django import template
from django.conf import settings
from dealer.git import git

register = template.Library()

@register.simple_tag
def revision():
    if settings.DEBUG:
      channel = 'staging' if settings.STAGING else 'dev'
      return '#%s @%s' % (git.revision, channel)
