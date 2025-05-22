from django import template

from ..models import MenuName

register = template.Library()


@register.inclusion_tag('the_menu_app/this_is_the_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    """
    Функция формирует списки всех уровней меню до указанного текущим и возвращает всё меню в шаблон.
    """
    current_menu = MenuName.objects.get(name=menu_name).points.all().values()  # все пункты указанного меню
    upper_level = current_menu.filter(above=None)  # верхний уровень меню

    # текущий уровень с деревом по основному стволу в глубину
    # до того уровня, который был выбран самым нижним
    family_tree = None
    if menu_name in context.request.GET:  # проверяет запрос: указано ли конкретное меню
        current_point = current_menu.get(id=context.request.GET[menu_name])  # текущий пункт меню из запроса
        submenu = current_menu.filter(above=current_point['id'])  # подпункты текущего пункта
        current_point['submenu'] = submenu  # добавляет текущему пункту его подуровень
        family_tree = current_point  # сохраняет текущий пункт с его подуровнем

        while family_tree['above_id'] is not None:  # работает пока у текущего пункта есть уровень над ним
            current_point = current_menu.get(id=family_tree['above_id'])  # пункт над предыдущим пунктом по дереву
            submenu = current_menu.filter(above=current_point['id'])  # пункты текущего уровня
            for current_level_point in submenu:  # проход по пунктам текущего уровня
                # находит пункт над предыдущим пунктом в текущем уровнем и добавляет ему всё дерево подпунктов
                if current_level_point['id'] == family_tree['id']:
                    current_level_point['submenu'] = family_tree['submenu']
            current_point['submenu'] = submenu  # добавляет текущему пункту всё дерево подпунктов
            family_tree = current_point  # сохраняет текущий пункт со всем деревом подпунктов

        for upper_level_point in upper_level:  # проход по верхнему уровню
            # находит пункт, где начинается ветвление и добавляет ему всё дерево
            if upper_level_point['id'] == family_tree['id']:
                upper_level_point['submenu'] = family_tree['submenu']

    # возвращается только верхний уровень если меню не указано.
    # Если указано, то всё дерево.
    return {'menu': upper_level, 'menu_name': menu_name}
