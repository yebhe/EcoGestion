<template>
    <div class="password-reset-container">
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <h2 class="title">Réinitialiser votre mot de passe</h2>
      <form @submit.prevent="resetPassword" class="password-form">
        <div class="form-group">
          <label for="new_password">Nouveau mot de passe</label>
          <input
            type="password"
            v-model="newPassword"
            required
            placeholder="Entrez votre nouveau mot de passe"
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label for="confirm_password">Confirmer le mot de passe</label>
          <input
            type="password"
            v-model="confirmPassword"
            required
            placeholder="Confirmez votre nouveau mot de passe"
            class="form-input"
          />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" :disabled="loading" class="submit-button">
          {{ loading ? "Veuillez patienter..." : "Réinitialiser le mot de passe" }}
        </button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import { toast } from "vue3-toastify";
  import Swal from "sweetalert2";
import router from "../router";
  
  export default {
    data() {
      return {
        newPassword: "",
        confirmPassword: "",
        error: "",
        loading: false,
      };
    },
    methods: {
      async resetPassword() {
        this.error = "";
  
        if (this.newPassword !== this.confirmPassword) {
          this.error = "Les mots de passe ne correspondent pas.";
          return;
        }
  
        const { uidb64, token } = this.$route.params;
  
        this.loading = true;
  
        try {
          const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)?.[1];
  
          const response = await axios.put(
            `${import.meta.env.VITE_APP_BASE_URL_API}/password/reset/${uidb64}/${token}/`,
            {
              password: this.newPassword,
              re_password: this.confirmPassword,
            },
            {
              headers: {
                "X-CSRFToken": csrfToken,
              },
              withCredentials: true,
            }
          );
  
          Swal.fire({
            title: "Succès!",
            text: response.data.message,
            icon: "success",
          }).then(() => {
            router.push("/login").then(() => {
              toast("Mot de passe réinitialisé avec succès.", {
                theme: "auto",
                type: "success",
              });
            });
          });
        } catch (error) {
          if (error.response?.data?.error) {
            Swal.fire({
              title: "Erreur!",
              text: error.response.data.error,
              icon: "error",
            });
          } else {
            Swal.fire({
              title: "Erreur!",
              text: "Une erreur inattendue s'est produite. Veuillez réessayer.",
              icon: "error",
            });
          }
  
          router.push("/").catch(() => {});
        } finally {
          this.loading = false;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Source+Serif+Pro:wght@400;600&display=swap');
  
  .password-reset-container {
    font-family: 'Source Serif Pro', serif;
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
    color: #0A1128;
    background-color: #FEFCFB;
  }
  
  .title {
    text-align: center;
    color: #001F54;
    margin-bottom: 30px;
    font-weight: 600;
  }
  
  .password-form {
    background-color: #FEFCFB;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(10, 17, 40, 0.1);
    border: 1px solid rgba(18, 130, 162, 0.2);
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 8px;
    color: #034078;
    font-weight: 600;
  }
  
  .form-input {
    width: 100%;
    padding: 12px;
    border: 2px solid rgba(18, 130, 162, 0.3);
    border-radius: 4px;
    font-family: 'Source Serif Pro', serif;
    font-size: 16px;
    background-color: #FEFCFB;
    color: #0A1128;
    transition: all 0.3s ease;
  }
  
  .form-input:focus {
    outline: none;
    border-color: #1282A2;
    box-shadow: 0 0 5px rgba(18, 130, 162, 0.2);
  }
  
  .submit-button {
    width: 100%;
    padding: 12px;
    background-color: #034078;
    color: #FEFCFB;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    font-family: 'Source Serif Pro', serif;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .submit-button:hover:not(:disabled) {
    background-color: #001F54;
  }
  
  .submit-button:disabled {
    background-color: #0A1128;
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .error {
    color: #ff0000;
    font-size: 14px;
    margin-top: 5px;
    text-align: center;
  }
  
  ::placeholder {
    color: rgba(10, 17, 40, 0.5);
  }
  </style>
  