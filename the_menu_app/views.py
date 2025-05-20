from django.views.generic import TemplateView


class DisplayTheEntireSite(TemplateView):
    template_name = 'the_menu_app/index.html'
