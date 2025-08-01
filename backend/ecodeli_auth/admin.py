from datetime import datetime
from django.contrib import admin, messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, redirect
from .models import User
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


@admin.register(User)
class CustomUser(admin.ModelAdmin):
    list_display = ('email', 'status', 'is_active', 'username', 'phone_number', 'first_name', 'last_name', 'approve_button', 'reject_button')
    list_filter = ('status', 'is_active',)
    search_fields = ('email', 'status', 'first_name', 'last_name', 'phone_number', 'username',)
    readonly_fields = ('last_login', 'date_joined', 'username')
    actions = ['approve_users', 'reject_users', 'send_provisional_password']  

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(status='approved')
        return queryset

    @admin.action(description='Approuvé les utilisateurs selectionnés')
    def approve_users(self, request, queryset):
        for user in queryset:
            if user.status == 'approved':
                messages.info(request, f"Le compte de {user.email} a déjà été approuvé.")

            if user.status != 'approved':
                user.status = 'approved'
                user.is_active = True
                user.save()

                uidb64 = urlsafe_base64_encode(str(user.id).encode())
                token = PasswordResetTokenGenerator().make_token(user)
                # reset_password_link = f"https://yebhe.online/password/reset/{uidb64}/{token}/"
                reset_password_link = f"http://127.0.0.1:8000/password/reset/{uidb64}/{token}/"

                # Prepare the HTML message
                current_year = datetime.now().year
                try:
                    html_message = render_to_string('emails/reset_password.html', {
                        'user': user,
                        'reset_password_link': reset_password_link,
                        'current_year': current_year
                    })

                    # Send the email
                    email = EmailMessage(
                        subject="Digital Car, Compte approuvé - Lien de modification de mot de passe",
                        body=html_message,  
                        from_email=settings.EMAIL_HOST_USER,
                        to=[user.email],
                    )
                    email.content_subtype = "html"
                    email.send(fail_silently=False)

                    # Success message
                    messages.success(request, f"Le compte de {user.email} a été approuvé et un email a été envoyé.")
                except Exception as e:
                    messages.error(request, f"Erreur lors de l'envoi de l'email à {user.email}: {str(e)}")

    @admin.action(description='Rejeter les utilisateurs sélectionnés')
    def reject_users(self, request, queryset):
        for user in queryset:
            if user.status == 'rejected':
                messages.info(request, f"Le compte de {user.email} a déjà été rejeté.")

            if user.status != 'rejected':
                user.status = 'rejected'
                user.is_active = False
                user.save()
                current_year = datetime.now().year
                try:
                    html_message = render_to_string('emails/rejection_email.html', {
                        'user': user,
                        'current_year': current_year
                    })

                    # Send rejection email
                    email = EmailMessage(
                        subject='Digital Car, Votre inscription a été rejetée',
                        body=html_message,  
                        from_email=settings.EMAIL_HOST_USER,
                        to=[user.email],
                    )
                    email.content_subtype = "html"  # Send as HTML email
                    email.send(fail_silently=False)

                    messages.success(
                        request,
                        f"Le compte de {user.email} a été rejeté et un email a été envoyé.",
                    )
                except Exception as e:
                    messages.error(
                        request, f"Erreur lors de l'envoi de l'email à {user.email}: {str(e)}"
                    )

                messages.info(request, f"L'utilisateur {user.email} a été rejeté.")

    @admin.action(description='Envoyer un mot de passe provisoire aux utilisateurs sélectionnés')
    def send_provisional_password(self, request, queryset):
        for user in queryset:
            provisional_password = user.generate_provisional_password()

            user.is_active = True 
            user.save() 
            current_year = datetime.now().year
            try:
                html_message = render_to_string('emails/provisional_password_email.html', {
                    'user': user,
                    'provisional_password': provisional_password,
                    'current_year': current_year
                })

                email = EmailMessage(
                    subject='Digital Car, Votre mot de passe provisoire',
                    body=html_message,  
                    from_email=settings.EMAIL_HOST_USER,
                    to=[user.email],
                )
                email.content_subtype = "html" 
                email.send(fail_silently=False)

                messages.success(
                    request,
                    f"Le mot de passe provisoire a été envoyé à {user.email}.",
                )
            except Exception as e:
                messages.error(
                    request, f"Erreur lors de l'envoi du mot de passe provisoire à {user.email}: {e}"
                )

    def get_model_perms(self, request):
        """
        Only allow superusers to have full permissions.
        Other users see limited access.
        """
        if request.user.is_superuser:
            return super().get_model_perms(request)
        return {}

    def approve_button(self, obj):
        if obj.is_superuser:
            return "Aucune action"
        if obj.status != 'approved':
            return format_html(
                '<a class="button" href="{}">Approuver</a>',
                f"/admin/ecodeli_auth/user/{obj.id}/approve/"
            )
        return "Aucune action"

    approve_button.short_description = "Action" 
    approve_button.allow_tags = True

    def approve_user(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user.status == 'approved':
            messages.info(request, f"Le compte de {user.email} a déjà été approuvé.")
        if user.status != 'approved':
            user.status = 'approved'
            user.is_active = True
            user.generate_provisional_password()
            user.save()
            current_year = datetime.now().year


            try:
                uidb64 = urlsafe_base64_encode(str(user.id).encode())
                token = PasswordResetTokenGenerator().make_token(user)
                # reset_password_link = f"https://yebhe.online/password/reset/{uidb64}/{token}/"
                reset_password_link = f"http://127.0.0.1:8000/password/reset/{uidb64}/{token}/"
                
                html_message = render_to_string('emails/reset_password.html', {
                        'user': user,
                        'reset_password_link': reset_password_link,
                        'current_year': current_year
                    })

                email = EmailMessage(
                    subject="Digital Car, Compte approuvé - Lien de modification de mot de passe",
                    body=html_message,  
                    from_email=settings.EMAIL_HOST_USER,
                    to=[user.email],
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)

                messages.success(
                    request,
                    f"Le compte de {user.email} a été approuvé et un email a été envoyé.",
                )
            except Exception as e:
                messages.error(
                    request, f"Erreur lors de l'envoi de l'email à {user.email}: {e}"
                )
            return redirect(request.META.get('HTTP_REFERER', '/admin/'))

    def reject_button(self, obj):
        if obj.is_superuser:
            return "Aucune action"

        if obj.status != 'rejected':
            return format_html(
                '<a class="button" href="{}">Rejeter</a>',
                f"/admin/ecodeli_auth/user/{obj.id}/reject/"
            )

        return "Aucune action"

    reject_button.short_description = "Action" 
    reject_button.allow_tags = True

    def reject_user(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user.status == 'rejected':
            messages.info(request, f"Le compte de {user.email} a déjà été rejeté.")

        if user.status != 'rejected':
            user.status = 'rejected'
            user.is_active = False
            user.generate_provisional_password()
            user.save()

            current_year = datetime.now().year
            try:
                # Generate the rejection email content using the HTML template
                html_message = render_to_string('emails/rejection_email.html', {
                    'user': user,
                    'current_year': current_year
                })

                email = EmailMessage(
                    subject='Digital Car, Votre inscription a été rejetée',
                    body=html_message,  
                    from_email=settings.EMAIL_HOST_USER,
                    to=[user.email],
                )
                email.content_subtype = "html"  # Send as HTML email
                email.send(fail_silently=False)

                messages.success(
                    request,
                    f"Le compte de {user.email} a été rejeté et un email a été envoyé.",
                )
            except Exception as e:
                messages.error(
                    request, f"Erreur lors de l'envoi de l'email à {user.email}: {str(e)}"
                )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/'))

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/approve/', self.admin_site.admin_view(self.approve_user), name='approve-user'),
            path('<int:user_id>/reject/', self.admin_site.admin_view(self.reject_user), name='reject-user'),
        ]
        return custom_urls + urls

