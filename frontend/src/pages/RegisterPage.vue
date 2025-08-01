<template>
    <div class="register-container">
      <div class="register-card">
        <h1 class="register-title">Inscription</h1>
        
        <form @submit.prevent="handleSubmit" class="register-form">
          <div class="form-group">
            <label for="username">Nom d'utilisateur</label>
            <input 
              id="username" 
              v-model="formData.username" 
              type="text" 
              required 
              class="form-control"
              :class="{ 'is-invalid': errors.username }"
              :disabled="isSubmitting"
            />
            <div v-if="errors.username" class="invalid-feedback">{{ errors.username }}</div>
          </div>
    
          <div class="form-group">
            <label for="email">Email</label>
            <input 
              id="email" 
              v-model="formData.email" 
              type="email" 
              required 
              class="form-control"
              :class="{ 'is-invalid': errors.email }"
              :disabled="isSubmitting"
            />
            <div v-if="errors.email" class="invalid-feedback">{{ errors.email }}</div>
          </div>
    
          <div class="form-row">
            <div class="form-group col-md-6">
              <label for="first_name">Prénom</label>
              <input 
                id="first_name" 
                v-model="formData.first_name" 
                type="text" 
                required 
                class="form-control"
                :class="{ 'is-invalid': errors.first_name }"
                :disabled="isSubmitting"
              />
              <div v-if="errors.first_name" class="invalid-feedback">{{ errors.first_name }}</div>
            </div>
    
            <div class="form-group col-md-6">
              <label for="last_name">Nom</label>
              <input 
                id="last_name" 
                v-model="formData.last_name" 
                type="text" 
                required 
                class="form-control"
                :class="{ 'is-invalid': errors.last_name }"
                :disabled="isSubmitting"
              />
              <div v-if="errors.last_name" class="invalid-feedback">{{ errors.last_name }}</div>
            </div>
          </div>
    
          <div class="form-group">
            <label for="phone_number">Numéro de téléphone</label>
            <input 
              id="phone_number" 
              v-model="formData.phone_number" 
              type="tel" 
              required 
              class="form-control"
              :class="{ 'is-invalid': errors.phone_number }"
              :disabled="isSubmitting"
            />
            <div v-if="errors.phone_number" class="invalid-feedback">{{ errors.phone_number }}</div>
          </div>
    
          <div class="form-group">
            <label for="password">Mot de passe</label>
            <input 
              id="password" 
              v-model="formData.password" 
              type="password" 
              required 
              class="form-control"
              :class="{ 'is-invalid': errors.password }"
              :disabled="isSubmitting"
            />
            <div v-if="errors.password" class="invalid-feedback">{{ errors.password }}</div>
            <small class="form-text text-muted">
              Le mot de passe doit contenir au moins 8 caractères, incluant des lettres, des chiffres et des caractères spéciaux.
            </small>
          </div>
    
          <div class="form-group">
            <label for="confirm_password">Confirmer le mot de passe</label>
            <input 
              id="confirm_password" 
              v-model="confirmPassword" 
              type="password" 
              required 
              class="form-control"
              :class="{ 'is-invalid': errors.confirm_password }"
              :disabled="isSubmitting"
            />
            <div v-if="errors.confirm_password" class="invalid-feedback">{{ errors.confirm_password }}</div>
          </div>
    
          <div class="form-group user-type-group">
            <label>Type d'utilisateur</label>
            <select 
              id="user_type" 
              v-model="formData.user_type" 
              class="form-control"
              :class="{ 'is-invalid': errors.user_type }"
              :disabled="isSubmitting"
            >
              <option value="client">Client</option>
              <option value="commercant">Commerçant</option>
              <option value="prestataire">Prestataire de services</option>
              <option value="livreur">Livreur</option>
            </select>
            <div v-if="errors.user_type" class="invalid-feedback">{{ errors.user_type }}</div>
          </div>
    
          <div class="form-group form-check">
            <input 
              id="termsAgreement" 
              v-model="termsAgreed" 
              type="checkbox" 
              required 
              class="form-check-input"
              :class="{ 'is-invalid': errors.terms }"
              :disabled="isSubmitting"
            />
            <label for="termsAgreement" class="form-check-label">
              J'accepte les <a href="#" @click.prevent="showTerms">conditions d'utilisation</a>
            </label>
            <div v-if="errors.terms" class="invalid-feedback">{{ errors.terms }}</div>
          </div>
    
          <!-- Affichage des erreurs générales -->
          <div v-if="serverError" class="alert alert-danger">
            {{ serverError }}
          </div>
    
          <button 
            type="submit" 
            class="btn btn-primary btn-register" 
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            {{ isSubmitting ? 'Inscription en cours...' : 'S\'inscrire' }}
          </button>
        </form>
    
        <div class="login-link">
          Déjà un compte? <router-link to="/login">Se connecter</router-link>
        </div>
      </div>
    </div>
  </template>
    
  <script>
  import { ref, reactive, computed } from 'vue';
  import { useRouter } from 'vue-router';
  import { toast } from 'vue3-toastify';
  import Swal from 'sweetalert2';
  import axios from 'axios';
  import { useAuthStore } from '../store/authStore';
  
  export default {
    name: 'RegisterPage',
    setup() {
      const router = useRouter();
      const authStore = useAuthStore();
      const isSubmitting = ref(false);
      const serverError = ref('');
      const termsAgreed = ref(false);
      const confirmPassword = ref('');
  
      // Formulaire avec les noms de champs exactement comme attendus par l'API
      const formData = reactive({
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        phone_number: '',
        password: '',
        user_type: 'client'
      });
  
      // Erreurs du formulaire
      const errors = reactive({
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        phone_number: '',
        password: '',
        confirm_password: '',
        user_type: '',
        terms: ''
      });
  
      // Validation du formulaire
      const validateForm = () => {
        let isValid = true;
        
        // Réinitialiser toutes les erreurs
        Object.keys(errors).forEach(key => {
          errors[key] = '';
        });
        
        // Validation du nom d'utilisateur
        if (!formData.username.trim()) {
          errors.username = "Le nom d'utilisateur est requis";
          isValid = false;
        } else if (formData.username.length < 3) {
          errors.username = "Le nom d'utilisateur doit contenir au moins 3 caractères";
          isValid = false;
        }
  
        // Validation de l'email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!formData.email.trim()) {
          errors.email = "L'email est requis";
          isValid = false;
        } else if (!emailRegex.test(formData.email)) {
          errors.email = "Format d'email invalide";
          isValid = false;
        }
  
        // Validation du prénom
        if (!formData.first_name.trim()) {
          errors.first_name = "Le prénom est requis";
          isValid = false;
        }
  
        // Validation du nom
        if (!formData.last_name.trim()) {
          errors.last_name = "Le nom est requis";
          isValid = false;
        }
  
        // Validation du numéro de téléphone
        if (!formData.phone_number.trim()) {
          errors.phone_number = "Le numéro de téléphone est requis";
          isValid = false;
        }
  
        // Validation du mot de passe
        if (!formData.password) {
          errors.password = "Le mot de passe est requis";
          isValid = false;
        } else if (formData.password.length < 8) {
          errors.password = "Le mot de passe doit contenir au moins 8 caractères";
          isValid = false;
        }
  
        // Validation de la confirmation du mot de passe
        if (formData.password !== confirmPassword.value) {
          errors.confirm_password = "Les mots de passe ne correspondent pas";
          isValid = false;
        }
  
        // Validation des termes d'utilisation
        if (!termsAgreed.value) {
          errors.terms = "Vous devez accepter les conditions d'utilisation";
          isValid = false;
        }
  
        return isValid;
      };
  
      // Afficher les conditions d'utilisation
      const showTerms = () => {
        Swal.fire({
          title: "Conditions d'utilisation",
          html: `
            <div class="terms-container" style="text-align: left; max-height: 300px; overflow-y: auto; padding: 10px;">
              <h3>1. Acceptation des conditions</h3>
              <p>En vous inscrivant, vous acceptez toutes les conditions énoncées dans ce document.</p>
              
              <h3>2. Responsabilités des utilisateurs</h3>
              <p>Vous êtes responsable de maintenir la confidentialité de votre compte et mot de passe.</p>
              
              <h3>3. Confidentialité</h3>
              <p>Votre confidentialité est importante pour nous. Veuillez consulter notre politique de confidentialité pour plus d'informations.</p>
              
              <h3>4. Modification des services</h3>
              <p>Nous nous réservons le droit de modifier ou d'interrompre le service à tout moment.</p>
              
              <h3>5. Résiliation</h3>
              <p>Vous pouvez résilier votre compte à tout moment et pour n'importe quelle raison.</p>
            </div>
          `,
          showCancelButton: true,
          confirmButtonText: "J'accepte",
          cancelButtonText: "Je refuse",
          confirmButtonColor: "#28a745",
          cancelButtonColor: "#dc3545",
        }).then((result) => {
          if (result.isConfirmed) {
            termsAgreed.value = true;
          } else {
            termsAgreed.value = false;
          }
        });
      };
  
      // Gestion de la soumission du formulaire
      const handleSubmit = async () => {
        // Prevent multiple submissions
        if (isSubmitting.value) return;
  
        // Reset errors
        serverError.value = '';
        
        // Validate form
        if (!validateForm()) {
          toast("Veuillez corriger les erreurs dans le formulaire", {
            theme: "auto",
            type: "error",
          });
          return;
        }
  
        // Set submitting state
        isSubmitting.value = true;
  
        try {
          // Single registration attempt using auth store
          const result = await authStore.register(
            formData.username,
            formData.email,
            formData.password,
            formData.first_name,
            formData.last_name,
            formData.phone_number,
            formData.user_type
          );
  
          if (result && result.success) {
            // Reset form on successful registration
            resetForm();
          }
        } catch (error) {
          console.error("Erreur lors de l'inscription:", error);
          serverError.value = "Une erreur s'est produite lors de l'inscription. Veuillez réessayer.";
        } finally {
          // Always reset submitting state
          isSubmitting.value = false;
        }
      };
  
      // Réinitialiser le formulaire
      const resetForm = () => {
        Object.keys(formData).forEach(key => {
          formData[key] = key === 'user_type' ? 'client' : '';
        });
        
        confirmPassword.value = '';
        termsAgreed.value = false;
        
        Object.keys(errors).forEach(key => {
          errors[key] = '';
        });
        
        serverError.value = '';
      };
  
      return {
        formData,
        confirmPassword,
        termsAgreed,
        errors,
        isSubmitting,
        serverError,
        handleSubmit,
        showTerms
      };
    }
  }
  </script>
  
  
  <style scoped>
  .register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
    background-color: #f8f9fa;
  }
  
  .register-card {
    width: 100%;
    max-width: 600px;
    padding: 30px;
    border-radius: 10px;
    background-color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .register-title {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
  }
  
  .register-form {
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  .form-row {
    display: flex;
    flex-wrap: wrap;
    margin-right: -10px;
    margin-left: -10px;
  }
  
  .col-md-6 {
    flex: 0 0 50%;
    max-width: 50%;
    padding-right: 10px;
    padding-left: 10px;
  }
  
  .form-control {
    display: block;
    width: 100%;
    padding: 10px;
    font-size: 16px;
    line-height: 1.5;
    color: #495057;
    background-color: #fff;
    background-clip: padding-box;
    border: 1px solid #ced4da;
    border-radius: 4px;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  }
  
  .form-control:focus {
    border-color: #80bdff;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  }
  
  .form-control.is-invalid {
    border-color: #dc3545;
  }
  
  .invalid-feedback {
    display: block;
    width: 100%;
    margin-top: 5px;
    font-size: 14px;
    color: #dc3545;
  }
  
  .alert {
    padding: 12px;
    margin-bottom: 20px;
    border-radius: 4px;
  }
  
  .alert-danger {
    color: #721c24;
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
  }
  
  .form-check {
    position: relative;
    display: block;
    padding-left: 25px;
    margin-bottom: 10px;
  }
  
  .form-check-input {
    position: absolute;
    margin-top: 5px;
    margin-left: -25px;
  }
  
  .user-type-group {
    margin-top: 20px;
  }
  
  .btn {
    display: inline-block;
    font-weight: 500;
    text-align: center;
    white-space: nowrap;
    vertical-align: middle;
    user-select: none;
    border: 1px solid transparent;
    padding: 12px 20px;
    font-size: 16px;
    line-height: 1.5;
    border-radius: 4px;
    transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out;
    cursor: pointer;
  }
  
  .btn-primary {
    color: #fff;
    background-color: #007bff;
    border-color: #007bff;
  }
  
  .btn-primary:hover {
    color: #fff;
    background-color: #0069d9;
    border-color: #0062cc;
  }
  
  .btn-primary:disabled {
    color: #fff;
    background-color: #007bff;
    border-color: #007bff;
    opacity: 0.65;
    cursor: not-allowed;
  }
  
  .btn-register {
    width: 100%;
    margin-top: 20px;
  }
  
  .login-link {
    text-align: center;
    margin-top: 20px;
  }
  
  .login-link a {
    color: #007bff;
    text-decoration: none;
  }
  
  .login-link a:hover {
    text-decoration: underline;
  }
  
  .spinner-border {
    display: inline-block;
    width: 1rem;
    height: 1rem;
    border: 0.2em solid currentColor;
    border-right-color: transparent;
    border-radius: 50%;
    animation: spinner-border .75s linear infinite;
    margin-right: 8px;
  }
  
  @keyframes spinner-border {
    to { transform: rotate(360deg); }
  }
  
  @media (max-width: 768px) {
    .col-md-6 {
      flex: 0 0 100%;
      max-width: 100%;
    }
  }
  </style>