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
    """
    Функция формирует списки всех уровней меню до указанного текущим и возвращает всё меню в шаблон.
    """
    current_menu = MenuName.objects.get(name=menu_name).points.all()  # все пункты указанного меню
    upper_level = create_list_of_sublevel(current_menu)  # верхний уровень меню

    # список текущего уровня с деревом по основному стволу в глубину
    # до того уровня, который был выбран самым нижним
    family_tree = []
    if menu_name in context.request.GET:  # проверяет запрос: указано ли конкретное меню
        current_point = current_menu.get(id=context.request.GET[menu_name])  # текущий пункт меню из запроса
        submenu = create_list_of_sublevel(current_menu,current_point)  # подпункты текущего пункта
        # добавляет в список с деревом текущий пункт с его подуровнем
        family_tree.append({'current_point': current_point, 'submenu': submenu})

        while family_tree[0]['current_point'].above:  # работает пока у текущего пункта есть уровень над ним
            current_point = family_tree[0]['current_point'].above  # пункт над предыдущим пунктом по дереву
            submenu = create_list_of_sublevel(current_menu, current_point)  # пункты текущего уровня
            for current_level_point in submenu:  # проход по пунктам текущего уровня
                if current_level_point['current_point'] == family_tree[0]['current_point']:
                    # находит пункт над предыдущим в текущем уровнем и добавляет ему всё дерево подпунктов
                    current_level_point['submenu'] = family_tree[0]['submenu']
            family_tree.clear()  # стирает из переменной ссылку на дерево, она останется только в нужном пункте меню
            # теперь в этот список сохраняется всё дерево с надстроенным уровнем
            family_tree.append({'current_point': current_point, 'submenu': submenu})

        for upper_level_point in upper_level:  # проход по верхнему уровню
            if upper_level_point['current_point'] == family_tree[0]['current_point']:
                # находит пункт, где начинается ветвление и добавляет ему всё дерево
                upper_level_point['submenu'] = family_tree[0]['submenu']

    # возвращается только верхний уровень если меню не указано.
    # Если указано, то всё дерево.
    return {'menu': upper_level}
