# livraison/models.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class JustificatifType(models.Model):
    nom = models.CharField(_('nom'), max_length=100)
    description = models.TextField(_('description'))
    obligatoire = models.BooleanField(_('obligatoire'), default=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = _('type de justificatif')
        verbose_name_plural = _('types de justificatifs')

class ProfilLivreur(models.Model):
    """Informations spécifiques aux livreurs"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='profil_livreur',
        verbose_name=_('utilisateur')
    )
    adresse = models.TextField(_('adresse'), blank=True)
    ville = models.CharField(_('ville'), max_length=100, blank=True)
    code_postal = models.CharField(_('code postal'), max_length=10, blank=True)
    numero_immatriculation = models.CharField(_('numéro d\'immatriculation'), max_length=50, blank=True)
    description_vehicule = models.TextField(_('description du véhicule'), blank=True)
    rayon_action = models.IntegerField(_('rayon d\'action (km)'), default=20)
    capacite_poids_max = models.FloatField(_('capacité de poids maximale (kg)'), default=10)
    capacite_volume_max = models.FloatField(_('capacité de volume maximale (m³)'), default=0.5)
    iban = models.CharField(_('IBAN'), max_length=34, blank=True)
    disponible = models.BooleanField(_('disponible'), default=True)
    
    def __str__(self):
        return f"Profil livreur de {self.user.get_full_name() or self.user.username}"
    
    class Meta:
        verbose_name = _('profil livreur')
        verbose_name_plural = _('profils livreurs')

class Justificatif(models.Model):
    """Documents justificatifs fournis par le livreur"""
    livreur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='justificatifs',
        limit_choices_to={'user_type': 'livreur'},
        verbose_name=_('livreur')
    )
    type_justificatif = models.ForeignKey(
        JustificatifType, 
        on_delete=models.CASCADE,
        verbose_name=_('type de justificatif')
    )
    fichier = models.FileField(
        _('fichier'), 
        upload_to='justificatifs/', null=True, blank=True
    )
    date_upload = models.DateTimeField(
        _('date d\'upload'), 
        auto_now_add=True
    )
    statut = models.CharField(
        _('statut'), 
        max_length=20, 
        choices=[
            ('en_attente', _('En attente de validation')),
            ('valide', _('Validé')),
            ('rejete', _('Rejeté'))
        ], 
        default='en_attente'
    )
    commentaire_admin = models.TextField(_('commentaire administrateur'), blank=True)
    
    def __str__(self):
        return f"{self.type_justificatif.nom} - {self.livreur.get_full_name()}"
    
    class Meta:
        verbose_name = _('justificatif')
        verbose_name_plural = _('justificatifs')

class TrajetAnnonce(models.Model):
    """Trajets annoncés par le livreur"""
    livreur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='trajets_annonces',
        verbose_name=_('livreur')
    )
    photo_produit = models.ImageField(_('photo du produit'), upload_to='livraisons/', null=True, blank=True)
    adresse_depart = models.CharField(_('adresse de départ'), max_length=255)
    ville_depart = models.CharField(_('ville de départ'), max_length=100)
    code_postal_depart = models.CharField(_('code postal de départ'), max_length=10)
    adresse_arrivee = models.CharField(_('adresse d\'arrivée'), max_length=255)
    ville_arrivee = models.CharField(_('ville d\'arrivée'), max_length=100)
    code_postal_arrivee = models.CharField(_('code postal d\'arrivée'), max_length=10)
    date_depart = models.DateTimeField(_('date de départ'))
    date_arrivee = models.DateTimeField(_('date d\'arrivée'))
    capacite_poids = models.FloatField(_('capacité de poids disponible (kg)'), blank=True)
    capacite_volume = models.FloatField(_('capacité de volume disponible (m³)'), blank=True)
    commentaire = models.TextField(_('commentaire'), blank=True)
    date_creation = models.DateTimeField(_('date de création'), auto_now_add=True)
    
    montant = models.DecimalField(_('montant'), max_digits=10, decimal_places=2, null=True, blank=True, default=None)
    commission_plateforme = models.DecimalField(_('commission plateforme'), max_digits=10, decimal_places=2,null=True, blank=True, default=2)
    
    statut = models.CharField(
        _('statut'), 
        max_length=20, 
        choices=[
            ('actif', _('Actif')),
            ('selected', _('Selected')),
            ('annule', _('Annulé'))
        ], 
        default='actif'
    )
    
    def __str__(self):
        return f"{self.ville_depart} → {self.ville_arrivee} ({self.date_depart.strftime('%d/%m/%Y')})"
    
    class Meta:
        verbose_name = _('trajet annoncé')
        verbose_name_plural = _('trajets annoncés')

class Livraison(models.Model):
    """Livraisons effectuées par le livreur"""
    livreur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='livraisons',
        verbose_name=_('livreur')
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mes_livraisons',
        verbose_name=_('client'),
        null=True, blank=True
    )
    trajet_annonce = models.ForeignKey(
        TrajetAnnonce, 
        on_delete=models.SET_NULL, 
        related_name='livraisons',
        null=True, 
        blank=True,
        verbose_name=_('trajet annoncé')
    )
    statut = models.CharField(
        _('statut'), 
        max_length=20, 
        choices=[
            ('en_attente', _('En attente de confirmation')),
            ('confirmee', _('Confirmée')),
            ('en_preparation', _('En préparation')),
            ('en_cours', _('En cours')),
            ('livree', _('Livrée')),
            ('annulee', _('Annulée'))
        ], 
        default='en_attente'
    )
    
    commentaire_client = models.TextField(_('commentaire client'), null=True, blank=True, default=None)
    commentaire_livreur = models.TextField(_('commentaire livreur') , null=True, blank=True, default=None)
    
    def __str__(self):
        return f"Livraison #{self.id} - {self.statut}"
    
    class Meta:
        verbose_name = _('livraison')
        verbose_name_plural = _('livraisons')

class Paiement(models.Model):
    """Paiements effectués aux livreurs"""
    livreur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='paiements',
        limit_choices_to={'user_type': 'livreur'},
        verbose_name=_('livreur')
    )
    livraisons = models.ManyToManyField(
        Livraison, 
        related_name='paiements',
        verbose_name=_('livraisons')
    )
    date = models.DateTimeField(_('date'), auto_now_add=True)
    reference = models.CharField(_('référence'), max_length=100)
    statut = models.CharField(
        _('statut'), 
        max_length=20, 
        choices=[
            ('en_attente', _('En attente')),
            ('traite', _('Traité')),
            ('rejete', _('Rejeté'))
        ], 
        default='en_attente'
    )
    
    @property
    def montant(self):
        """Calcule le montant total du paiement en fonction des livraisons associées"""
        total = 0
        for livraison in self.livraisons.all():
            montant = float(livraison.montant) if livraison.montant is not None else 0
            total += montant
        return total
    
    @property
    def total_commission(self):
        """Calcule le total des commissions prélevées"""
        total = 0
        for livraison in self.livraisons.all():
            commission = float(livraison.commission_plateforme) if livraison.commission_plateforme is not None else 0
            total += commission
        return total
    
    def __str__(self):
        return f"Paiement #{self.reference} - {self.montant:.2f}€"
    
    class Meta:
        verbose_name = _('paiement')
        verbose_name_plural = _('paiements')
          
class Disponibilite(models.Model):
    """Disponibilités des livreurs"""
    livreur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='disponibilites',
        limit_choices_to={'user_type': 'livreur'},
        verbose_name=_('livreur')
    )
    date_debut = models.DateTimeField(_('date de début'))
    date_fin = models.DateTimeField(_('date de fin'))
    
    def __str__(self):
        return f"Disponibilité de {self.livreur.get_full_name()} du {self.date_debut} au {self.date_fin}"
    
    class Meta:
        verbose_name = _('disponibilité')
        verbose_name_plural = _('disponibilités')
        
        
        
class Facture(models.Model):
    """Factures avec système de séquestre"""
    numero = models.CharField(_('numéro'), max_length=50, unique=True)
    livraison = models.OneToOneField(Livraison, on_delete=models.CASCADE, related_name='facture')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='factures')
    
    # Montants
    montant_ht = models.DecimalField(_('montant HT'), max_digits=10, decimal_places=2)
    taux_tva = models.DecimalField(_('taux TVA'), max_digits=5, decimal_places=2, default=20.00)
    montant_tva = models.DecimalField(_('montant TVA'), max_digits=10, decimal_places=2)
    montant_ttc = models.DecimalField(_('montant TTC'), max_digits=10, decimal_places=2)
    
    # Dates
    date_creation = models.DateTimeField(_('date de création'), auto_now_add=True)
    date_echeance = models.DateTimeField(_('date d\'échéance'))
    date_paiement_client = models.DateTimeField(_('date paiement client'), null=True, blank=True)
    date_liberation_fonds = models.DateTimeField(_('date libération fonds'), null=True, blank=True)
    
    # Système de séquestre
    statut = models.CharField(
        _('statut'),
        max_length=25,
        choices=[
            ('en_attente', _('En attente de paiement')),
            ('fonds_bloques', _('Fonds bloqués (séquestre)')),
            ('en_attente_confirmation', _('En attente de confirmation')),
            ('fonds_liberes', _('Fonds libérés au livreur')),
            ('litige', _('En litige')),
            ('rembourse', _('Remboursé au client')),
            ('annulee', _('Annulée'))
        ],
        default='en_attente'
    )
    
    # Stripe
    stripe_payment_intent_id = models.CharField(_('ID Payment Intent Stripe'), max_length=200, null=True, blank=True)
    
    # Confirmations
    confirmation_livraison_livreur = models.BooleanField(_('Livraison confirmée par livreur'), default=False)
    confirmation_reception_client = models.BooleanField(_('Réception confirmée par client'), default=False)
    date_confirmation_livreur = models.DateTimeField(_('Date confirmation livreur'), null=True, blank=True)
    date_confirmation_client = models.DateTimeField(_('Date confirmation client'), null=True, blank=True)
    
    # Délai automatique
    delai_auto_liberation = models.DateTimeField(_('Délai auto-libération'), null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = f"FAC-{uuid.uuid4().hex[:8].upper()}"
        
        if self.montant_ht:
            self.montant_tva = (self.montant_ht * self.taux_tva) / 100
            self.montant_ttc = self.montant_ht + self.montant_tva
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Facture {self.numero} - {self.get_statut_display()}"
    
    class Meta:
        verbose_name = _('facture')
        verbose_name_plural = _('factures')
        ordering = ['-date_creation']

class CompteLivreur(models.Model):
    """Compte Stripe du livreur"""
    livreur = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='compte_livreur'
    )
    
    nom_titulaire = models.CharField(_('Nom du titulaire'), max_length=100)
    stripe_account_id = models.CharField(_('ID Compte Stripe'), max_length=200, blank=True)
    stripe_verified = models.BooleanField(_('Compte vérifié'), default=False)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Compte de {self.livreur.get_full_name()}"

class PaiementLivreur(models.Model):
    """Paiements versés aux livreurs"""
    livreur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='paiements_recus')
    facture = models.OneToOneField(Facture, on_delete=models.CASCADE, related_name='paiement_livreur')
    
    montant_brut = models.DecimalField(_('Montant brut'), max_digits=10, decimal_places=2)
    commission_plateforme = models.DecimalField(_('Commission plateforme'), max_digits=10, decimal_places=2)
    montant_net = models.DecimalField(_('Montant net versé'), max_digits=10, decimal_places=2)
    
    stripe_transfer_id = models.CharField(_('ID Transfer Stripe'), max_length=200)
    
    statut = models.CharField(
        max_length=20,
        choices=[
            ('en_cours', _('En cours')),
            ('complete', _('Terminé')),
            ('echec', _('Échec'))
        ],
        default='en_cours'
    )
    
    date_paiement = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Paiement {self.montant_net}€ à {self.livreur.get_full_name()}"

class Notification(models.Model):
    """Notifications pour les utilisateurs"""
    destinataire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField(_('titre'), max_length=200)
    message = models.TextField(_('message'))
    type_notification = models.CharField(
        _('type'),
        max_length=20,
        choices=[
            ('paiement', _('Paiement')),
            ('livraison', _('Livraison')),
            ('confirmation', _('Confirmation')),
            ('litige', _('Litige')),
            ('liberation', _('Libération de fonds'))
        ]
    )
    lue = models.BooleanField(_('lue'), default=False)
    date_creation = models.DateTimeField(_('date création'), auto_now_add=True)
    
    class Meta:
        ordering = ['-date_creation']
        
        
    
    
    
    