from re import A
from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.ProfilLivreur)
admin.site.register(models.JustificatifType)
admin.site.register(models.Justificatif)
admin.site.register(models.TrajetAnnonce)
admin.site.register(models.Livraison)
admin.site.register(models.Paiement)
admin.site.register(models.Disponibilite)
