# monapp/admin.py
from django.contrib import admin
from .models import Departement, Environnement, Serveur, Role, ServeurRole

@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('nom',)  # Affiche le champ 'nom' dans la liste
    search_fields = ('nom',)  # Permet la recherche par 'nom'

@admin.register(Environnement)
class EnvironnementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'departement')  # Affiche les champs 'nom' et 'departement' dans la liste
    search_fields = ('nom',)  # Permet la recherche par 'nom'
    list_filter = ('departement',)  # Ajoute un filtre pour le champ 'departement'

@admin.register(Serveur)
class ServeurAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'IP', 'domain', 'environnement')  # Affiche les champs dans la liste
    search_fields = ('hostname', 'IP')  # Permet la recherche par 'hostname' et 'IP'
    list_filter = ('environnement',)  # Ajoute un filtre pour le champ 'environnement'

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('nom',)  # Affiche le champ 'nom' dans la liste
    search_fields = ('nom',)  # Permet la recherche par 'nom'

@admin.register(ServeurRole)
class ServeurRoleAdmin(admin.ModelAdmin):
    list_display = ('serveur', 'role')  # Affiche les champs 'serveur' et 'role' dans la liste
    search_fields = ('serveur__hostname', 'role__nom')  # Permet la recherche par 'hostname' et 'role'
    list_filter = ('role',)  # Ajoute un filtre pour le champ 'role'
