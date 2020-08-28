from django import template

register = template.Library()

@register.filter()
def subtract(value, arg):
    if value:
        return '{:.2f}'.format(value - arg)

