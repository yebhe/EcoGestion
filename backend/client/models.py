from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class ProfilClient(models.Model):
    """Modèle représentant le profil d'un client"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profil_client'
    )
    telephone = models.CharField(_("Numéro de téléphone"), max_length=20)
    date_naissance = models.DateField(_("Date de naissance"), null=True, blank=True)
    photo_profil = models.ImageField(_("Photo de profil"), upload_to='clients/photos/', null=True, blank=True)
    notification_email = models.BooleanField(_("Notifications par email"), default=True)
    notification_sms = models.BooleanField(_("Notifications par SMS"), default=False)
    notification_push = models.BooleanField(_("Notifications push"), default=True)
    created_at = models.DateTimeField(_("Date de création"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date de mise à jour"), auto_now=True)

    class Meta:
        verbose_name = _("Profil client")
        verbose_name_plural = _("Profils clients")

    def __str__(self):
        return f"Profil de {self.user.username}"


class AdresseLivraison(models.Model):
    """Modèle représentant une adresse de livraison d'un client"""
    client = models.ForeignKey(
        ProfilClient, 
        on_delete=models.CASCADE, 
        related_name='adresses'
    )
    nom_adresse = models.CharField(_("Nom de l'adresse"), max_length=50)  # ex: "Domicile", "Bureau"
    destinataire = models.CharField(_("Nom du destinataire"), max_length=100)
    adresse = models.CharField(_("Adresse"), max_length=255)
    complement_adresse = models.CharField(_("Complément d'adresse"), max_length=255, blank=True, null=True)
    code_postal = models.CharField(_("Code postal"), max_length=10)
    ville = models.CharField(_("Ville"), max_length=100)
    pays = models.CharField(_("Pays"), max_length=100, default="France")
    instructions_speciales = models.TextField(_("Instructions spéciales"), blank=True, null=True)
    par_defaut = models.BooleanField(_("Adresse par défaut"), default=False)
    created_at = models.DateTimeField(_("Date de création"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date de mise à jour"), auto_now=True)

    class Meta:
        verbose_name = _("Adresse de livraison")
        verbose_name_plural = _("Adresses de livraison")

    def __str__(self):
        return f"{self.nom_adresse} - {self.ville}"

    def save(self, *args, **kwargs):
        # Si l'adresse est définie par défaut, désactiver les autres adresses par défaut
        if self.par_defaut:
            AdresseLivraison.objects.filter(
                client=self.client, 
                par_defaut=True
            ).exclude(pk=self.pk).update(par_defaut=False)
        super().save(*args, **kwargs)


class AnnonceClient(models.Model):
    """Modèle représentant une annonce créée par un client"""
    TYPE_CHOICES = [
        ('LIVRAISON', _('Livraison de colis')),
        ('TRANSPORT', _('Transport de personne')),
        ('SERVICE', _('Service à domicile')),
        ('ACHAT', _('Achat à l\'étranger')),
    ]
    
    STATUT_CHOICES = [
        ('ACTIVE', _('Active')),
        ('ATTRIBUEE', _('Attribuée')),
        ('EN_COURS', _('En cours')),
        ('TERMINEE', _('Terminée')),
        ('ANNULEE', _('Annulée')),
    ]
    
    client = models.ForeignKey(
        ProfilClient, 
        on_delete=models.CASCADE, 
        related_name='annonces'
    )
    type_annonce = models.CharField(_("Type d'annonce"), max_length=20, choices=TYPE_CHOICES)
    titre = models.CharField(_("Titre"), max_length=100)
    description = models.TextField(_("Description"))
    prix_propose = models.DecimalField(_("Prix proposé"), max_digits=10, decimal_places=2)
    adresse_depart = models.ForeignKey(
        AdresseLivraison, 
        on_delete=models.SET_NULL, 
        related_name='annonces_depart',
        null=True,
        blank=True
    )
    adresse_arrivee = models.ForeignKey(
        AdresseLivraison, 
        on_delete=models.SET_NULL, 
        related_name='annonces_arrivee',
        null=True
    )
    date_souhaitee = models.DateField(_("Date souhaitée"))
    heure_souhaitee = models.TimeField(_("Heure souhaitée"), null=True, blank=True)
    statut = models.CharField(_("Statut"), max_length=20, choices=STATUT_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(_("Date de création"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date de mise à jour"), auto_now=True)

    class Meta:
        verbose_name = _("Annonce client")
        verbose_name_plural = _("Annonces clients")

    def __str__(self):
        return f"{self.titre} ({self.get_type_annonce_display()})"


class Colis(models.Model):
    """Modèle représentant un colis à livrer"""
    TAILLE_CHOICES = [
        ('XS', _('Très petit (enveloppe)')),
        ('S', _('Petit')),
        ('M', _('Moyen')),
        ('L', _('Grand')),
        ('XL', _('Très grand'))
    ]
    
    annonce = models.OneToOneField(
        AnnonceClient, 
        on_delete=models.CASCADE, 
        related_name='colis',
        null=True,
        blank=True
    )
    taille = models.CharField(_("Taille"), max_length=2, choices=TAILLE_CHOICES)
    poids = models.DecimalField(_("Poids (kg)"), max_digits=5, decimal_places=2)
    longueur = models.IntegerField(_("Longueur (cm)"), null=True, blank=True)
    largeur = models.IntegerField(_("Largeur (cm)"), null=True, blank=True)
    hauteur = models.IntegerField(_("Hauteur (cm)"), null=True, blank=True)
    contenu = models.TextField(_("Description du contenu"))
    fragile = models.BooleanField(_("Colis fragile"), default=False)
    photo = models.ImageField(_("Photo du colis"), upload_to='colis/photos/', null=True, blank=True)
    instructions_speciales = models.TextField(_("Instructions spéciales"), blank=True, null=True)
    assurance_souhaitee = models.BooleanField(_("Assurance souhaitée"), default=False)
    valeur_declaree = models.DecimalField(_("Valeur déclarée (€)"), max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(_("Date de création"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date de mise à jour"), auto_now=True)

    class Meta:
        verbose_name = _("Colis")
        verbose_name_plural = _("Colis")

    def __str__(self):
        return f"Colis {self.id} - {self.get_taille_display()}"


class CommandeClient(models.Model):
    """Modèle représentant une commande passée par un client"""
    STATUT_CHOICES = [
        ('ATTENTE_PAIEMENT', _('En attente de paiement')),
        ('PAIEMENT_CONFIRME', _('Paiement confirmé')),
        ('EN_PREPARATION', _('En préparation')),
        ('EN_COURS_LIVRAISON', _('En cours de livraison')),
        ('LIVREE', _('Livrée')),
        ('ANNULEE', _('Annulée')),
    ]
    
    client = models.ForeignKey(
        ProfilClient, 
        on_delete=models.CASCADE, 
        related_name='commandes'
    )
    annonce = models.ForeignKey(
        AnnonceClient, 
        on_delete=models.SET_NULL, 
        related_name='commandes',
        null=True,
        blank=True
    )
    reference = models.CharField(_("Référence"), max_length=20, unique=True)
    montant_total = models.DecimalField(_("Montant total"), max_digits=10, decimal_places=2)
    statut = models.CharField(_("Statut"), max_length=20, choices=STATUT_CHOICES, default='ATTENTE_PAIEMENT')
    stripe_payment_intent = models.CharField(_("Stripe Payment Intent ID"), max_length=255, blank=True, null=True)
    date_paiement = models.DateTimeField(_("Date de paiement"), null=True, blank=True)
    adresse_livraison = models.ForeignKey(
        AdresseLivraison, 
        on_delete=models.SET_NULL, 
        related_name='commandes',
        null=True
    )
    created_at = models.DateTimeField(_("Date de création"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date de mise à jour"), auto_now=True)

    class Meta:
        verbose_name = _("Commande client")
        verbose_name_plural = _("Commandes clients")

    def __str__(self):
        return f"Commande {self.reference}"


class FactureClient(models.Model):
    """Modèle représentant une facture client"""
    STATUT_CHOICES = [
        ('EMISE', _('Émise')),
        ('PAYEE', _('Payée')),
        ('ANNULEE', _('Annulée')),
    ]
    
    commande = models.OneToOneField(
        CommandeClient, 
        on_delete=models.CASCADE, 
        related_name='facture'
    )
    numero_facture = models.CharField(_("Numéro de facture"), max_length=20, unique=True)
    date_emission = models.DateField(_("Date d'émission"), auto_now_add=True)
    date_echeance = models.DateField(_("Date d'échéance"))
    montant_ht = models.DecimalField(_("Montant HT"), max_digits=10, decimal_places=2)
    montant_tva = models.DecimalField(_("Montant TVA"), max_digits=10, decimal_places=2)
    montant_ttc = models.DecimalField(_("Montant TTC"), max_digits=10, decimal_places=2)
    statut = models.CharField(_("Statut"), max_length=10, choices=STATUT_CHOICES, default='EMISE')
    fichier_pdf = models.FileField(_("Fichier PDF"), upload_to='factures/clients/', null=True, blank=True)
    
    class Meta:
        verbose_name = _("Facture client")
        verbose_name_plural = _("Factures clients")

    def __str__(self):
        return f"Facture {self.numero_facture}"


class SuiviColis(models.Model):
    """Modèle représentant les étapes de suivi d'un colis"""
    STATUT_CHOICES = [
        ('PRIS_EN_CHARGE', _('Pris en charge')),
        ('EN_TRANSIT', _('En transit')),
        ('EN_ENTREPOT', _('En entrepôt')),
        ('EN_LIVRAISON', _('En livraison')),
        ('LIVRE', _('Livré')),
        ('INCIDENT', _('Incident')),
    ]
    
    colis = models.ForeignKey(
        Colis, 
        on_delete=models.CASCADE, 
        related_name='evenements_suivi'
    )
    statut = models.CharField(_("Statut"), max_length=20, choices=STATUT_CHOICES)
    date_evenement = models.DateTimeField(_("Date de l'événement"), auto_now_add=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    localisation = models.CharField(_("Localisation"), max_length=255, blank=True, null=True)
    latitude = models.DecimalField(_("Latitude"), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_("Longitude"), max_digits=9, decimal_places=6, null=True, blank=True)
    photo_preuve = models.ImageField(_("Photo preuve"), upload_to='suivi/photos/', null=True, blank=True)
    
    class Meta:
        verbose_name = _("Suivi de colis")
        verbose_name_plural = _("Suivis de colis")
        ordering = ['-date_evenement']

    def __str__(self):
        return f"Suivi colis {self.colis.id} - {self.get_statut_display()}"


class EvaluationClient(models.Model):
    """Modèle représentant une évaluation donnée par un client"""
    client = models.ForeignKey(
        ProfilClient, 
        on_delete=models.CASCADE, 
        related_name='evaluations'
    )
    commande = models.OneToOneField(
        CommandeClient, 
        on_delete=models.CASCADE, 
        related_name='evaluation'
    )
    note = models.IntegerField(_("Note"), choices=[(i, i) for i in range(1, 6)])
    commentaire = models.TextField(_("Commentaire"), blank=True, null=True)
    date_evaluation = models.DateTimeField(_("Date d'évaluation"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Évaluation client")
        verbose_name_plural = _("Évaluations clients")

    def __str__(self):
        return f"Évaluation de {self.client.user.username} - Note: {self.note}/5"