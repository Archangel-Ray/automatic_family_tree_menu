from django import template

from ..models import MenuPoint, MenuName

register = template.Library()


@register.inclusion_tag('the_menu_app/this_is_the_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    current_menu = MenuName.objects.get(name=menu_name).points.all()

    family_tree = []
    if menu_name in context.request.GET:
        current_point = current_menu.get(id=context.request.GET[menu_name])
        submenu = current_menu.filter(above=current_point)
        family_tree.append({'current_point': current_point, 'submenu': submenu})

    while family_tree[0]['current_point'].above:
        current_point = family_tree[0]['current_point'].above
        submenu = current_menu.filter(above=current_point.above)
        family_tree.insert(0, {'current_point': current_point, 'submenu': submenu})

    return {'menu': family_tree}
