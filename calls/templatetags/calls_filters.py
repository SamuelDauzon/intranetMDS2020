from django import template

register = template.Library()

@register.filter()
def rating_stars(value, with_empty_stars = True):
    if value:
        if with_empty_stars:
            return "⭐"*value+"⭒"*(10-value)
        else:
            return "⭐"*value
    else:
        return ""