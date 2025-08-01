from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone
import random
import string

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Le champ email est obligatoire'))
        
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            username=username, 
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('status', 'approved')
        extra_fields.setdefault('user_type', 'admin')
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Le superutilisateur doit avoir is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Le superutilisateur doit avoir is_superuser=True.'))
        
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('livreur', _('Livreur')),
        ('client', _('Client')),
        ('commercant', _('Commerçant')),
        ('prestataire', _('Prestataire de services')),
        # ('admin', _('Administrateur'))
    )
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    email = models.EmailField(
        _('adresse email'), 
        unique=True,
        error_messages={
            'unique': _("Un utilisateur avec cet email existe déjà.")
        }
    )
    username = models.CharField(
        _('nom d\'utilisateur'), 
        max_length=150, 
        unique=True,
        error_messages={
            'unique': _("Un utilisateur avec ce nom d'utilisateur existe déjà.")
        }
    )
    first_name = models.CharField(
        _('prénom'), 
        max_length=150, 
        blank=True
    )
    last_name = models.CharField(
        _('nom de famille'), 
        max_length=150, 
        blank=True
    )
    
    # Champs personnalisés
    user_type = models.CharField(
        _('type d\'utilisateur'), 
        max_length=20, 
        choices=USER_TYPE_CHOICES,
        default='client',
        help_text=_('Sélectionnez le type de compte utilisateur')
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )
    phone_number = models.CharField(
        _('numéro de téléphone'), 
        max_length=20, 
        blank=True, 
        null=True,
        help_text=_('Votre numéro de téléphone pour les contacts')
    )
    profile_image = models.ImageField(
        _('image de profil'), 
        upload_to='profile_images/', 
        null=True, 
        blank=True,
        help_text=_('Téléchargez une image de profil (optionnel)')
    )
    
    # Champs standard Django
    is_staff = models.BooleanField(
        _('statut personnel'), 
        default=False,
        help_text=_('Détermine si l\'utilisateur peut accéder à l\'interface d\'administration.')
    )
    is_active = models.BooleanField(
        _('actif'), 
        default=True,
        help_text=_('Détermine si ce compte utilisateur doit être traité comme actif.')
    )
    is_verified = models.BooleanField(
        _('vérifié'), 
        default=False,
        help_text=_('Indique si l\'utilisateur a vérifié son adresse email.')
    )
    date_joined = models.DateTimeField(
        _('date d\'inscription'), 
        default=timezone.now
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def generate_provisional_password(self):
        provisional_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        self.set_password(provisional_password)  
        self.provisional_password = provisional_password
        self.save()
        return provisional_password

    def generate_approval_code(self):
            """Generate a random code for approval."""
            approval_code = ''.join(random.choices(string.ascii_letters + string.digits, k=12))  # Adjust length as needed
            self.approval_code = approval_code
            self.save()
            return approval_code

    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.email

class VerificationToken(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='verification_token',
        verbose_name=_('utilisateur')
    )
    token = models.CharField(
        max_length=255, 
        unique=True,
        verbose_name=_('jeton de vérification')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('créé le')
    )
    expires_at = models.DateTimeField(
        verbose_name=_('expire le')
    )

    def is_valid(self):
        return timezone.now() <= self.expires_at

    def __str__(self):
        return f"Jeton de vérification pour {self.user.email}"

    class Meta:
        verbose_name = _('jeton de vérification')
        verbose_name_plural = _('jetons de vérification')