from django.db import models


class MenuName(models.Model):
    name = models.CharField(unique=True)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name


class MenuPoint(models.Model):
    point = models.CharField()
    menu = models.ForeignKey(MenuName, blank=True, related_name='points', on_delete=models.CASCADE)
    above = models.ForeignKey('self', blank=True, null=True, related_name='submenu', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'пункт'
        verbose_name_plural = 'пункты'

    def __str__(self):
        return self.point
