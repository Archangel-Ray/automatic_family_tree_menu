from django import template

from ..models import MenuPoint, MenuName

register = template.Library()


@register.inclusion_tag('the_menu_app/this_is_the_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    current_menu = MenuName.objects.get(name=menu_name).points.all()
    upper_level = [{'current_point': x} for x in list(current_menu.filter(above=None))]
    family_tree = []
    if menu_name in context.request.GET:
        current_point = current_menu.get(id=context.request.GET[menu_name])
        submenu = [{'current_point': x} for x in list(current_menu.filter(above=current_point))]
        family_tree.append({'current_point': current_point, 'submenu': submenu})

        while family_tree[0]['current_point'].above:
            current_point = family_tree[0]['current_point'].above
            submenu = [{'current_point': x} for x in list(current_menu.filter(above=current_point))]
            for current_level_point in submenu:
                if current_level_point['current_point'] == family_tree[0]['current_point']:
                    current_level_point['submenu'] = family_tree[0]['submenu']
            family_tree.clear()
            family_tree.append({'current_point': current_point, 'submenu': submenu})

        for upper_level_point in upper_level:
            if upper_level_point['current_point'] == family_tree[0]['current_point']:
                upper_level_point['submenu'] = family_tree[0]['submenu']

    return {'menu': upper_level}
