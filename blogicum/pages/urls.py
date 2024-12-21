from django.urls import path
from . import views

app_name = 'pages'

handler403 = 'core.views.custom_handler403'
handler404 = 'core.views.custom_handler404'
handler500 = 'core.views.custom_handler500'

urlpatterns = [
    path('pages/about/', views.AboutView.as_view(), name='about'),
    path('pages/rules/', views.RulesView.as_view(), name='rules'),
]
