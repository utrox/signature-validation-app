import datetime
from django import template
from django.template.loader import render_to_string

register = template.Library()

   
@register.simple_tag(takes_context=True)
def render_component(context, template_name):
    return render_to_string(template_name, context.flatten())

@register.simple_tag
def current_date():
    return datetime.datetime.now().strftime("%Y.%m.%d")
