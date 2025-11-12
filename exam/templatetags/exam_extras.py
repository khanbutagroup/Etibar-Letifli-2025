from django import template

register = template.Library()

@register.filter
def get_field(obj, attr_name):
    """Model obyektindən dinamik atribut alır."""
    return getattr(obj, attr_name, None)

@register.filter
def attr(obj, attr_name):
    """`obj.attr_name` şəklində dinamik atribut götürür (məsələn `is_correct_a` və s.)."""
    return getattr(obj, attr_name, None)
