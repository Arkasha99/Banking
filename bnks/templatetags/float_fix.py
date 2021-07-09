from django import template

register = template.Library()

@register.filter(name='float_fix')
def float_fix(value):
    return f"{value:.{3}f}"
