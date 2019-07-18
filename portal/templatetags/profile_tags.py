from django import template
from ..models import Profile

register = template.Library()

#@register.simple_tag(name='my_tag') Para un nombre diferente
@register.simple_tag()
def total_profiles():
    return Profile.objects.all().count()