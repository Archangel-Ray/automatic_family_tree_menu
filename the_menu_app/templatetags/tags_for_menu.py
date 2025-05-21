from django import template

from ..models import MenuPoint, MenuName

register = template.Library()


def create_list_of_sublevel(all_menu_points, above=None):
    """
    Получает все пункты меню, выбирает из них те которые привязаны к указанному пункту формируя Queryset его подпунктов.
    Переводит Queryset в список словарей, где устанавливает название, по которому обращаться к этому пункту. Это нужно
    было, чтобы потом добавить этому пункту атрибут со списком его подуровня. Теоретически список с пунктами подуровня
    можно хранить в базе и обновлять при добавлении или удалении пунктов. Но такого в задании не было, по этому я так
    не сделал. Такой вариант сократил бы время отрисовки меню ровно на эту функцию. Оно затрачивалось бы в момент
    добавления или удаления пункта в меню во время работы с базой.
    """
    sublevel = all_menu_points.filter(above=above)
    list_of_sublevel = list()
    for point in sublevel:
        list_of_sublevel.append({'current_point': point})

    return list_of_sublevel


@register.inclusion_tag('the_menu_app/this_is_the_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    current_menu = MenuName.objects.get(name=menu_name).points.all()
    upper_level = create_list_of_sublevel(current_menu)
    family_tree = []
    if menu_name in context.request.GET:
        current_point = current_menu.get(id=context.request.GET[menu_name])
        submenu = create_list_of_sublevel(current_menu,current_point)
        family_tree.append({'current_point': current_point, 'submenu': submenu})

        while family_tree[0]['current_point'].above:
            current_point = family_tree[0]['current_point'].above
            submenu = create_list_of_sublevel(current_menu, current_point)
            for current_level_point in submenu:
                if current_level_point['current_point'] == family_tree[0]['current_point']:
                    current_level_point['submenu'] = family_tree[0]['submenu']
            family_tree.clear()
            family_tree.append({'current_point': current_point, 'submenu': submenu})

        for upper_level_point in upper_level:
            if upper_level_point['current_point'] == family_tree[0]['current_point']:
                upper_level_point['submenu'] = family_tree[0]['submenu']

    return {'menu': upper_level}
