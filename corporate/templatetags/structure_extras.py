from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key"""
    return dictionary.get(key)

@register.filter
def multiply(value, arg):
    """Multiply two values"""
    try:
        return float(value) * float(arg)
    except (TypeError, ValueError):
        return 0
