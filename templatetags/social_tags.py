from django import template
from tools.models import Social

register = template.Library()



# Social snippets
@register.inclusion_tag('tools/tags/social.html', takes_context=True)
def social_icons(context):
    return {
        'social_icons': Social.objects.all(),
        'request': context['request'],
    }