from django import template

register = template.Library()


@register.filter
def split(value, arg):
    """Split a string by the given separator."""
    if value:
        return value.split(arg)
    return []


@register.filter
def trim(value):
    """Remove leading and trailing whitespace."""
    if value:
        return value.strip()
    return value


@register.filter
def filter_root_entries(entries):
    """Filter entries to only include root entries (those without a parent)."""
    return [entry for entry in entries if not entry.parent]
