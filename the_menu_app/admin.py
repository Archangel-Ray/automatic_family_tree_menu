from django.contrib import admin

from .models import MenuName, MenuPoint


@admin.register(MenuPoint)
class MenuPointAdmin(admin.ModelAdmin):
    list_display = ['point', 'above', 'menu']
    ordering = ['menu', 'above', 'point']
    list_filter = ['above']


@admin.register(MenuName)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name']
