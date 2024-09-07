from django.db import models

class Departement(models.Model):
    nom = models.CharField(max_length=100, unique=True, null=False)
    
    def __str__(self):
        return self.nom

class Environnement(models.Model):
    nom = models.CharField(max_length=50, unique=True, null=False)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name='environnements')
    
    def __str__(self):
        return self.nom

class Serveur(models.Model):
    hostname = models.CharField(max_length=255, null=False)
    IP = models.CharField(max_length=15, null=False)
    domain = models.CharField(max_length=255, null=False)
    environnement = models.ForeignKey(Environnement, on_delete=models.CASCADE, related_name='serveurs')

    def __str__(self):
        return self.hostname

class Role(models.Model):
    nom = models.CharField(max_length=50, unique=True, null=False)
    
    def __str__(self):
        return self.nom

class ServeurRole(models.Model):
    serveur = models.ForeignKey(Serveur, on_delete=models.CASCADE, related_name='roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='serveurs')
