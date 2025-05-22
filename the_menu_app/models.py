from django.db import models


class MenuName(models.Model):
    """
    Здесь только название меню. Меню может быть несколько.
    У каждого пункта выбирается к какому меню он будет принадлежать.
    """
    name = models.CharField(unique=True)

    class Meta:
        verbose_name = 'Название меню'
        verbose_name_plural = 'Названия меню'

    def __str__(self):
        return self.name


class MenuPoint(models.Model):
    """
    Все пункты всех меню.
    """
    # Подпись пункта
    point = models.CharField()
    # Меню к которому этот пункт прикреплён
    menu = models.ForeignKey(MenuName, blank=True, related_name='points', on_delete=models.CASCADE)
    # Пункт под которым прикрепляется этот пункт
    above = models.ForeignKey('self', blank=True, null=True, related_name='submenu', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'пункт'
        verbose_name_plural = 'пункты'

    def __str__(self):
        return self.point
