from django import template

register = template.Library()


@register.inclusion_tag('knowledge/entry_tree.html')
def entry_tree(entries, active_slug=None, current_slug=None, depth=0):
    """Render entries in a nested tree structure"""
    # Filter root entries (those without parent)
    root_entries = [e for e in entries if e.parent_id is None]
    
    return {
        'entries': root_entries,
        'all_entries': entries,
        'active_slug': active_slug,
        'current_slug': current_slug,
        'depth': depth,
    }


def get_children(entry, all_entries):
    """Get direct children of an entry"""
    return [e for e in all_entries if e.parent_id == entry.id]
