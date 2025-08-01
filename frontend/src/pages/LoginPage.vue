<template>
    <div class="login-container">
      <div class="login-card">
        <h1 class="login-title">Connexion</h1>
        
        <form @submit.prevent="handleSubmit" class="login-form">
          <div class="form-group">
            <label for="email">Email</label>
            <input 
              id="email" 
              v-model="email" 
              type="email" 
              required 
              class="form-control"
              :class="{ 'is-invalid': errors.email }"
            />
            <div v-if="errors.email" class="invalid-feedback">{{ errors.email }}</div>
          </div>
  
          <div class="form-group">
            <label for="password">Mot de passe</label>
            <div class="password-input-group">
              <input 
                id="password" 
                v-model="password" 
                :type="showPassword ? 'text' : 'password'" 
                required 
                class="form-control"
                :class="{ 'is-invalid': errors.password }"
              />
              <button 
                type="button"
                class="password-toggle"
                @click="togglePasswordVisibility"
                tabindex="-1"
              >
                {{ showPassword ? 'Cacher' : 'Voir' }}
              </button>
            </div>
            <div v-if="errors.password" class="invalid-feedback">{{ errors.password }}</div>
          </div>
  
          <div class="form-options">
            <div class="form-check">
              <input 
                id="rememberMe" 
                v-model="rememberMe" 
                type="checkbox" 
                class="form-check-input"
              />
              <label for="rememberMe" class="form-check-label">Se souvenir de moi</label>
            </div>
            <router-link to="/forgot-password" class="forgot-password-link">
              Mot de passe oublié?
            </router-link>
          </div>
  
          <button 
            type="submit" 
            class="btn btn-primary btn-login" 
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            {{ isSubmitting ? 'Connexion en cours...' : 'Se connecter' }}
          </button>
        </form>
  
        <div class="register-link">
          Pas encore de compte? <router-link to="/register">S'inscrire</router-link>
        </div>
        
        <div class="status-info">
          <h3>Statut du compte</h3>
          <p>Après inscription, le processus d'activation se déroule en deux étapes :</p>
          <ol>
            <li><strong>Activation :</strong> Via le lien envoyé par email</li>
            <li><strong>Approbation :</strong> Par un administrateur du système</li>
          </ol>
          <p>Vous ne pourrez vous connecter qu'après ces deux étapes.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive } from 'vue';
  import { useRouter } from 'vue-router';
  import { toast } from 'vue3-toastify';
  import { useAuthStore } from '../store/authStore';
  
  export default {
    name: 'LoginPage',
    setup() {
      const authStore = useAuthStore();
      const router = useRouter();
  
      // Form fields
      const email = ref('');
      const password = ref('');
      const rememberMe = ref(false);
      const showPassword = ref(false);
      const isSubmitting = ref(false);
  
      // Form errors
      const errors = reactive({
        email: '',
        password: ''
      });
  
      // Toggle password visibility
      const togglePasswordVisibility = () => {
        showPassword.value = !showPassword.value;
      };
  
      // Validate form
      const validateForm = () => {
        let isValid = true;
        
        // Reset all errors
        Object.keys(errors).forEach(key => {
          errors[key] = '';
        });
        
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email.value || email.value.trim() === '') {
          errors.email = "L'email est requis";
          isValid = false;
        } else if (!emailRegex.test(email.value)) {
          errors.email = "Format d'email invalide";
          isValid = false;
        }
  
        // Password validation
        if (!password.value) {
          errors.password = "Le mot de passe est requis";
          isValid = false;
        }
  
        return isValid;
      };
  
      // Handle form submission
      const handleSubmit = async () => {
        if (!validateForm()) {
          toast("Veuillez corriger les erreurs dans le formulaire", {
            theme: "auto",
            type: "error",
          });
          return;
        }
  
        isSubmitting.value = true;
  
        try {
          const result = await authStore.login(email.value, password.value);
          
          if (result && result.success) {
            // Redirection is handled in the store
          }
        } catch (error) {
          console.error("Erreur lors de la connexion:", error);
          toast("Une erreur s'est produite lors de la connexion. Veuillez réessayer.", {
            theme: "auto",
            type: "error",
          });
        } finally {
          isSubmitting.value = false;
        }
      };
  
      return {
        email,
        password,
        rememberMe,
        showPassword,
        isSubmitting,
        errors,
        togglePasswordVisibility,
        handleSubmit
      };
    }
  }
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
    background-color: #f8f9fa;
  }
  
  .login-card {
    width: 100%;
    max-width: 450px;
    padding: 30px;
    border-radius: 10px;
    background-color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .login-title {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
  }
  
  .login-form {
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 20px;
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
  
  .password-input-group {
    position: relative;
  }
  
  .password-toggle {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: #6c757d;
    cursor: pointer;
  }
  
  .password-toggle:hover {
    color: #007bff;
  }
  
  .form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .form-check {
    display: flex;
    align-items: center;
  }
  
  .form-check-input {
    margin-right: 8px;
  }
  
  .forgot-password-link {
    color: #007bff;
    text-decoration: none;
  }
  
  .forgot-password-link:hover {
    text-decoration: underline;
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
  
  .btn-login {
    width: 100%;
    margin-top: 10px;
  }
  
  .register-link {
    text-align: center;
    margin-top: 20px;
  }
  
  .register-link a {
    color: #007bff;
    text-decoration: none;
  }
  
  .register-link a:hover {
    text-decoration: underline;
  }
  
  .status-info {
    margin-top: 30px;
    padding: 15px;
    border-radius: 5px;
    background-color: #f8f9fa;
    border-left: 4px solid #17a2b8;
  }
  
  .status-info h3 {
    font-size: 18px;
    margin-bottom: 10px;
    color: #17a2b8;
  }
  
  .status-info p {
    margin-bottom: 10px;
    font-size: 14px;
  }
  
  .status-info ol {
    padding-left: 20px;
    margin-bottom: 10px;
  }
  
  .status-info li {
    margin-bottom: 5px;
    font-size: 14px;
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
  </style>