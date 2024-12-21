from django.views.generic import TemplateView

from django.shortcuts import render


def custom_handler403(request, reason=None):
    context = {
        'reason': reason
    }
    return render(request, 'pages/403csrf.html', context, status=403)


def custom_handler404(request, exception):
    return render(request, 'pages/404.html', status=404)


def custom_handler500(request):
    return render(request, 'pages/500.html', status=500)


class AboutView(TemplateView):
    template_name = "pages/about.html"


class RulesView(TemplateView):
    template_name = "pages/rules.html"
