"""Template tags of the ``generic_positions`` app."""
from django.contrib.admin.templatetags.admin_list import result_list
from django.contrib.contenttypes.models import ContentType
from django.template import Library
from django.utils.safestring import mark_safe

from ..models import ObjectPosition

register = Library()


@register.inclusion_tag("admin/change_list_results.html")
def position_result_list(cl):
    """
    Displays the headers and data list together
    """
    result = result_list(cl)
    # Remove sortable attributes
    for x in range(0, len(result['result_headers'])):
        result['result_headers'][x]['sorted'] = False
        if result['result_headers'][x]['sortable']:
            result['result_headers'][x]['class_attrib'] = mark_safe(
                ' class="sortable"')
    # Append position <th> element
    result['result_headers'].append({
        'url_remove': '?o=',
        'sort_priority': 1,
        'sortable': True,
        'class_attrib': mark_safe(' class="sortable sorted ascending"'),
        'sorted': True,
        'text': 'position',
        'ascending': True,
        'url_primary': '?o=-1',
        'url_toggle': '?o=-1',
    })
    # Append the editable field to every result item
    for x in range(0, len(result['results'])):
        obj = cl.result_list[x]
        c_type = ContentType.objects.get_for_model(obj)
        # Get or create position object
        try:
            object_position = ObjectPosition.objects.get(
                content_type__pk=c_type.id, object_id=obj.id)
        except ObjectPosition.DoesNotExist:
            object_position = ObjectPosition.objects.create(
                content_object=obj, position=x)
        # Add the <td>
        html = ('<td><input class="vTextField" id="id_position-{0}"'
                ' maxlength="256" name="position-{0}" type="position"'
                ' value="{1}" /></td>').format(object_position.id,
                                               object_position.position)
        result['results'][x].append(mark_safe(html))
    return result