from django.urls import path, re_path

from . import views

app_name = 'pnm'

urlpatterns = [
    path('pandora-next-usage/', views.PandoraNextAccountUsageView.as_view(), name='pandora-next-usage'),
]
