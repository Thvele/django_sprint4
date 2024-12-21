from django.views.generic import TemplateView

# Представления для статичных страниц
class AboutView(TemplateView):
    template_name = "pages/about.html"

class RulesView(TemplateView):
    template_name = "pages/rules.html"
