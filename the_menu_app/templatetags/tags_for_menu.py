from django import template

from ..models import MenuPoint, MenuName

register = template.Library()


@register.inclusion_tag('the_menu_app/this_is_the_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    current_menu = MenuName.objects.get(name=menu_name).points.all()
    family_tree = []
    if menu_name in context.request.GET:
        family_tree.append(current_menu.get(id=context.request.GET[menu_name]))
    while family_tree[0].above:
        family_tree.insert(0, family_tree[0].above)
    return {'menu': family_tree}
