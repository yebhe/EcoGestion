from django.shortcuts import render

# Create your views here.
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


from .serializers import (
    UserModelCreateSerializer, 
    UserModelSerializer, 
    UserModelUpdatePasswordSerializer, 
    CustomUserUpdateSerializer, 
    PasswordUpdateSerializer
)


class UserRegistrationView(APIView):
    permission_classes = [AllowAny] 
    
    def post(self, request):
        data = request.data
        serializer = UserModelCreateSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            if user and not user.is_active:
                # Générer un lien d'activation
                uidb64 = urlsafe_base64_encode(str(user.id).encode())
                token = default_token_generator.make_token(user)
                activation_url = request.build_absolute_uri(
                    reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
                )

                # Envoyer l'email d'activation
                try:
                    html_message = render_to_string('emails/inscription_email.html', {
                        'user': user,
                        'activation_url': activation_url,
                    })
                    email = EmailMessage(
                        subject="Inscription réussie - Lien d'activation",
                        body=html_message,
                        from_email=settings.EMAIL_HOST_USER,
                        to=[user.email],
                    )
                    email.content_subtype = "html"
                    email.send(fail_silently=False)
                    
                except Exception as e:
                    # Log l'erreur sans bloquer l'inscription
                    print(f"Erreur d'envoi d'email : {str(e)}")

                return Response({
                    "message": "Utilisateur enregistré avec succès ! Un email de confirmation a été envoyé.",
                    "user_id": user.id
                }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"detail": "Email et mot de passe sont requis."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {"detail": "Identifiants invalides"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # # Gestion des différents cas de connexion
        # if user.status != 'approved':
        #     return Response({
        #         "detail": "Votre compte n'est pas encore approuvé. Veuillez attendre l'approbation de l'administrateur."
        #     }, status=status.HTTP_403_FORBIDDEN)

        # Générer les tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        return Response({
            "access": access_token,
            "refresh": str(refresh),
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'status': user.status,
                'is_superuser': user.is_superuser,
                'user_type': user.user_type
            }
        }, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserModelSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class AccountActivateView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request, uidb64, token): 
        try: 
            uid = urlsafe_base64_decode(uidb64).decode() 
            user = get_user_model().objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return redirect("/activation/result?message=Le lien d'activation est invalide !")

        if default_token_generator.check_token(user, token):
            if user.is_active:
                return redirect("/activation/result?message=Ce compte est déjà activé.")

            user.is_active = True
            user.is_verified = True
            user.save()
            try:
                html_message = render_to_string('emails/activation_email.html', {
                    'user': user,
                })

                email = EmailMessage(
                    subject="Votre compte a été activé",
                    body=html_message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[user.email],
                )

                email.content_subtype = "html"
                email.send(fail_silently=False)
            except Exception as e:
                print(f"Error sending email: {str(e)}")
            return redirect("/activation/result?message=Votre compte a été activé avec succès !")
        else:
            return redirect("/activation/result?message=Le lien d'activation est invalide ou expiré !")


class CustomPasswordResetConfirmView(APIView):
    def get(self, request, uidb64, token, *args, **kwargs):
        return redirect(f"/password-reset/{uidb64}/{token}/")
    def put(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(id=uid)
        except (TypeError, ValueError, get_user_model().DoesNotExist):
            return Response({"error": "Lien de réinitialisation invalide."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Jeton invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserModelUpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 

        user.set_password(serializer.validated_data['password'])
        user.save()

        try:
            html_message = render_to_string('emails/password_reset_success.html', {'user': user})
            email = EmailMessage(
                subject="Votre mot de passe a été réinitialisé avec succès",
                body=html_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'e-mail : {str(e)}")

        return Response(
            {"message": "Votre mot de passe a été réinitialisé avec succès."},
            status=status.HTTP_200_OK
        )
  

class UpdateUserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = CustomUserUpdateSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = CustomUserUpdateSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            profile = serializer.save()

            try:
                # Email à l'administrateur
                html_message_admin = render_to_string('emails/profile_email_admin.html', {
                    'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'email': profile.email,
                })
                email_admin = EmailMessage(
                    subject=f"Mise à jour de profil : {profile.first_name}",
                    body=html_message_admin,
                    from_email=settings.EMAIL_HOST_USER,  
                    to=[settings.EMAIL_HOST_USER], 
                )
                email_admin.content_subtype = "html" 
                email_admin.send(fail_silently=False) 

                # Email à l'utilisateur
                html_message_user = render_to_string('emails/profile_email_user.html', {
                    'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'email': profile.email,
                })
                email_user = EmailMessage(
                    subject="Mise à jour de votre profil",
                    body=html_message_user,
                    from_email=settings.EMAIL_HOST_USER,  
                    to=[profile.email], 
                )
                email_user.content_subtype = "html" 
                email_user.send(fail_silently=False)  

            except Exception as e:
                print(f"Erreur lors de l'envoi des emails : {str(e)}")

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        
        # Vérification du statut
        if user.status != 'approved':
            return Response(
                {"detail": "Seuls les utilisateurs approuvés peuvent mettre à jour leur mot de passe."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Récupération des données
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # Vérification de l'ancien mot de passe
        if not check_password(old_password, user.password):
            return Response(
                {"old_password_error": "L'ancien mot de passe est incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérification de la correspondance des nouveaux mots de passe
        if new_password != confirm_password:
            return Response(
                {"confirm_password_error": "Les mots de passe doivent correspondre."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Utilisation du serializer pour la validation finale
        serializer = PasswordUpdateSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Mot de passe mis à jour avec succès."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)