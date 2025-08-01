<template>
    <div class="update-password-container">
      <div class="form-card">
        <h2 class="title">Mettre à jour votre mot de passe</h2>
        <form @submit.prevent="updatePassword" class="password-form">
          <div class="form-group">
            <label for="oldPassword">Ancien mot de passe</label>
            <input
              type="password"
              id="oldPassword"
              v-model="oldPassword"
              :class="{'input-error': errors.oldPassword}"
              class="form-input"
            />
            <p v-if="errors.oldPassword" class="error-text">{{ errors.oldPassword }}</p>
          </div>
  
          <div class="form-group">
            <label for="newPassword">Nouveau mot de passe</label>
            <input
              type="password"
              id="newPassword"
              v-model="newPassword"
              :class="{'input-error': errors.newPassword}"
              class="form-input"
            />
            <p v-if="errors.newPassword" class="error-text">{{ errors.newPassword }}</p>
          </div>
  
          <div class="form-group">
            <label for="confirmPassword">Confirmer le mot de passe</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="confirmPassword"
              :class="{'input-error': errors.confirmPassword}"
              class="form-input"
            />
            <p v-if="errors.confirmPassword" class="error-text">{{ errors.confirmPassword }}</p>
          </div>
  
          <button type="submit" class="submit-btn">
            Mettre à jour
            <span class="btn-animation"></span>
          </button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  // Le script reste identique
  import axios from 'axios';
  import { toast } from 'vue3-toastify';
import router from '../router';
import { useAuthStore } from '../store/authStore';
  
  export default {
    data() {
      return {
        oldPassword: '',
        newPassword: '',
        confirmPassword: '',
        errors: {
          oldPassword: '',
          newPassword: '',
          confirmPassword: '',
        },
      };
    },
    methods: {
      validateForm() {
        this.errors = {
          oldPassword: '',
          newPassword: '',
          confirmPassword: '',
        };
  
        let valid = true;
        let errorMessages = [];
  
        if (!this.oldPassword) {
          this.errors.oldPassword = "L'ancien mot de passe est obligatoire.";
          errorMessages.push("Ancien mot de passe");
          valid = false;
        }
  
        if (!this.newPassword) {
          this.errors.newPassword = "Le nouveau mot de passe est obligatoire.";
          errorMessages.push("Nouveau mot de passe");
          valid = false;
        } else if (this.newPassword.length < 8) {
          this.errors.newPassword = "Le mot de passe doit contenir au moins 8 caractères.";
          errorMessages.push("Nouveau mot de passe");
          valid = false;
        }
  
        if (!this.confirmPassword) {
          this.errors.confirmPassword = "La confirmation du mot de passe est obligatoire.";
          errorMessages.push("Confirmation du mot de passe");
          valid = false;
        } else if (this.newPassword !== this.confirmPassword) {
          this.errors.confirmPassword = "Les mots de passe ne correspondent pas.";
          errorMessages.push("Confirmation du mot de passe");
          valid = false;
        }
  
        if (!valid && errorMessages.length > 0) {
          toast.error(`Veuillez remplir tous les champs s'ils vous plait !`, { theme: "auto" });
        }
  
        return valid;
      },
  
      async updatePassword() {
        if (!this.validateForm()) {
          return;
        }
  
        try {
          const token = localStorage.getItem('accessToken');
          if (!token) {
            toast.error("Token manquant, veuillez vous reconnecter.", { theme: "auto" });
            return;
          }
  
          const response = await axios.post(
            'http://localhost:8000/user/update-password/',
            {
              old_password: this.oldPassword,
              new_password: this.newPassword,
              confirm_password: this.confirmPassword,
            },
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
  
          const user = useAuthStore().user;

          const roleRedirectMap = {
            admin: '/admin-dashboard',
            client: '/client-dashboard',
            livreur: '/livreur-dashboard',
            commercant: '/commercant-dashboard',
            prestataire: '/prestataire-dashboard',
          };

          const dashboardRoute = roleRedirectMap[user?.user_type];

          router.push(dashboardRoute).then(() => {
            toast.success(response.data.message || "Mot de passe mis à jour avec succès.", { theme: "auto" });
          });

  
          this.resetForm();
        } catch (error) {
          if (error.response && error.response.data) {
            if (error.response.data?.detail){
              const user = useAuthStore().user;
              const dashboardRoute = user && user.is_superuser ? '/admin-dashboard' : '/user-dashboard';
  
              router.push(dashboardRoute).then(() => {
                toast.info(error.response.data?.detail, {theme: "auto"});
              });
            }
            const errorData = error.response.data;
  
            if (errorData.old_password_error) {
              this.errors.oldPassword = errorData.old_password_error;
            }
            if (errorData.confirm_password_error) {
              this.errors.confirmPassword = errorData.confirm_password_error;
            }
            if (errorData.new_password_error) {
              this.errors.newPassword = errorData.new_password_error;
            }
  
            if (errorData.message) {
              toast.error(errorData.message, { theme: "auto" });
            }
          } else {
            toast.error("Une erreur est survenue, veuillez réessayer.", { theme: "auto" });
          }
        }
      },
  
      resetForm() {
        this.oldPassword = '';
        this.newPassword = '';
        this.confirmPassword = '';
        this.errors = {
          oldPassword: '',
          newPassword: '',
          confirmPassword: '',
        };
      },
    },
  };
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Source+Serif+Pro:wght@400;600;700&display=swap');
  
  .update-password-container {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #001F54;
    font-family: 'Source Serif Pro', serif;
    padding: 20px;
  }
  
  .form-card {
    background-color: #FEFCFB;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 8px 24px rgba(10, 17, 40, 0.1);
    width: 100%;
    max-width: 400px;
    transform: translateY(20px);
    animation: slideUp 0.5s ease forwards;
  }
  
  .title {
    color: #0A1128;
    text-align: center;
    margin-bottom: 2rem;
    font-size: 1.8rem;
    font-weight: 600;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  label {
    display: block;
    color: white;
    margin-bottom: 0.5rem;
    font-weight: 600;
    font-size: 0.9rem;
  }
  
  .form-input {
    width: 100%;
    padding: 0.8rem;
    border: 2px solid #1282A2;
    border-radius: 6px;
    background-color: white;
    transition: all 0.3s ease;
    font-size: 1rem;
    color: #0A1128;
  }
  
  .form-input:focus {
    outline: none;
    border-color: #034078;
    box-shadow: 0 0 0 3px rgba(3, 64, 120, 0.1);
  }
  
  .input-error {
    border-color: #ff4444;
  }
  
  .error-text {
    color: #ff4444;
    font-size: 0.8rem;
    margin-top: 0.3rem;
    animation: shake 0.5s ease;
  }
  
  .submit-btn {
    width: 100%;
    padding: 1rem;
    background-color: #1282A2;
    color: #FEFCFB;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
  }
  
  .submit-btn:hover {
    background-color: #034078;
    transform: translateY(-2px);
  }
  
  .submit-btn:active {
    transform: translateY(0);
  }
  
  .btn-animation {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.6s ease, height 0.6s ease;
  }
  
  .submit-btn:hover .btn-animation {
    width: 300px;
    height: 300px;
  }
  
  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
  }
  
  @media (max-width: 480px) {
    .form-card {
      padding: 1.5rem;
    }
  
    .title {
      font-size: 1.5rem;
    }
  
    .form-input {
      padding: 0.7rem;
    }
  
    .submit-btn {
      padding: 0.8rem;
    }
  }
  </style>
  