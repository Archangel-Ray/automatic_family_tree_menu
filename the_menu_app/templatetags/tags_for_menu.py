from django import template

from ..models import MenuPoint

register = template.Library()


@register.inclusion_tag('the_menu_app/this_is_the_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    current_menu = {'menu': MenuPoint.objects.filter(menu__name=menu_name)}
    return current_menu
