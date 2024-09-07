from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('environnements/', views.environnement_list, name='environnement_stats'),
    path('environnements/<int:id>/', views.environnement_details, name='environnement_details'),
    path('serveurs/<int:id>/', views.serveur_details, name='serveur_details'),

]