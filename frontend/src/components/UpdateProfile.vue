<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-6">
      <div class="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-8">
        <h2 class="text-3xl font-bold mb-8 text-center text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">
          Mettre à jour votre profil
        </h2>
  
        <form @submit.prevent="validateAndSubmit" class="space-y-6">
          <!-- Champs du formulaire -->
          <div class="grid gap-6">
            <!-- Email -->
            <div>
              <label for="email" class="block text-white text-sm font-medium mb-2">Email</label>
              <input
                type="email"
                id="email"
                v-model="userData.email"
                @blur="validateEmail"
                class="w-full px-4 py-2 rounded-lg border focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-300"
                :class="{ 'border-red-300': errors.email }"
              />
              <span v-if="errors.email" class="mt-1 text-sm text-red-500">{{ errors.email }}</span>
            </div>
  
            <!-- Prénom -->
            <div>
              <label for="first_name" class="block text-white text-sm font-medium mb-2">Prénom</label>
              <input
                type="text"
                id="first_name"
                v-model="userData.first_name"
                @blur="validateFirstName"
                class="w-full px-4 py-2 rounded-lg border focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-300"
                :class="{ 'border-red-300': errors.first_name }"
              />
              <span v-if="errors.first_name" class="mt-1 text-sm text-red-500">{{ errors.first_name }}</span>
            </div>
  
            <!-- Nom -->
            <div>
              <label for="last_name" class="block text-white text-sm font-medium mb-2">Nom</label>
              <input
                type="text"
                id="last_name"
                v-model="userData.last_name"
                @blur="validateLastName"
                class="w-full px-4 py-2 rounded-lg border focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-300"
                :class="{ 'border-red-300': errors.last_name }"
              />
              <span v-if="errors.last_name" class="mt-1 text-sm text-red-500">{{ errors.last_name }}</span>
            </div>
  
            <!-- Nom d'utilisateur -->
            <div>
              <label for="username" class="block text-white text-sm font-medium mb-2">Nom d'utilisateur</label>
              <input
                type="text"
                id="username"
                v-model="userData.username"
                @blur="validateUsername"
                class="w-full px-4 py-2 rounded-lg border focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-300"
                :class="{ 'border-red-300': errors.username }"
              />
              <span v-if="errors.username" class="mt-1 text-sm text-red-500">{{ errors.username }}</span>
            </div>
          </div>
  
          <br>
          <br>
          <!-- Bouton de soumission -->
          <button
            type="submit"
            class="btn btn-primary">
  
            Mettre à jour
          </button>
        </form>
      </div>
    </div>
  </template>
  <script>
  import axios from "axios";
  import { toast } from 'vue3-toastify';
  import router from '@/router';
  import { useAuthStore } from '@/store/authStore';
  
  
  export default {
    data() {
      return {
        userData: {
          email: "",
          first_name: "",
          last_name: "",
          username: "",
        },
        errors: {
          email: null,
          first_name: null,
          last_name: null,
          username: null,
        },
      };
    },
    methods: {
      validateEmail() {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!this.userData.email) {
          this.errors.email = "L'email est requis.";
        } else if (!emailRegex.test(this.userData.email)) {
          this.errors.email = "Email invalide.";
        } else {
          this.errors.email = null;
        }
      },
  
      validateFirstName() {
        if (!this.userData.first_name) {
          this.errors.first_name = "Le prénom est requis.";
        } else {
          this.errors.first_name = null;
        }
      },
  
      validateLastName() {
        if (!this.userData.last_name) {
          this.errors.last_name = "Le nom est requis.";
        } else {
          this.errors.last_name = null;
        }
      },
  
      validateUsername() {
        if (!this.userData.username) {
          this.errors.username = "Le nom d'utilisateur est requis.";
        } else {
          this.errors.username = null;
        }
      },
  
      validateAndSubmit() {
        this.validateEmail();
        this.validateFirstName();
        this.validateLastName();
        this.validateUsername();
  
        if (!this.errors.email && !this.errors.first_name &&
            !this.errors.last_name && !this.errors.username) {
          this.updateUser();
        } else {
          toast("Veuillez corriger les erreurs dans le formulaire.", {
            theme: "auto",
            type: "info",
          });
        }
      },
  
      async updateUser() {
        const formData = new FormData();
        formData.append("email", this.userData.email);
        formData.append("first_name", this.userData.first_name);
        formData.append("last_name", this.userData.last_name);
        formData.append("username", this.userData.username);
  
        try {
          const token = localStorage.getItem("accessToken");
          await axios.put(
            "http://localhost:8000/user/update-user-info/",
            formData,
            {
              headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "multipart/form-data",
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
            toast("Profil mis à jour avec succès.", {
                theme: "auto",
                type: "success",
            });
        });

        } catch (error) {
          toast("Erreur lors de la mise à jour.", {
            theme: "auto",
            type: "error",
          });
          console.error('Erreur:', error.response?.data || error.message);
        }
      },
    },
    async mounted() {
      try {
        const token = localStorage.getItem("accessToken");
        const response = await axios.get("http://localhost:8000/user/user/me/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
  
        this.userData = response.data;
      } catch (error) {
        toast("Erreur lors du chargement des informations utilisateur.", {
          theme: "auto",
          type: "info",
        });
        console.error(error);
      }
    },
  };
  </script>
  
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Source+Serif+Pro:wght@400;600;700&display=swap');
  
  .min-h-screen {
    min-height: 100vh;
    background: linear-gradient(135deg, #FEFCFB 0%, #1282A2 100%);
    font-family: 'Source Serif Pro', serif;
    padding: 2rem 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .max-w-2xl {
    width: 100%;
    max-width: 42rem;
    margin: 0 auto;
  }
  
  .bg-white {
    background: #FEFCFB;
    border-radius: 1rem;
    box-shadow: 0 10px 30px rgba(10, 17, 40, 0.1);
    padding: 2rem;
    position: relative;
    overflow: hidden;
  }
  
  /* Animation d'engrenage en arrière-plan */
  .bg-white::before {
    content: '';
    position: absolute;
    top: -50px;
    right: -50px;
    width: 100px;
    height: 100px;
    background: #034078;
    opacity: 0.05;
    border-radius: 50%;
    animation: rotate 10s linear infinite;
  }
  
  @keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  
  h2 {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 2rem;
    text-align: center;
    background: linear-gradient(45deg, #001F54, #034078);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    position: relative;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  label {
    display: block;
    color: #0A1128;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }
  
  input {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid #034078;
    border-radius: 0.5rem;
    background: #FEFCFB;
    color: #0A1128;
    font-family: 'Source Serif Pro', serif;
    transition: all 0.3s ease;
  }
  
  input:focus {
    outline: none;
    border-color: #1282A2;
    box-shadow: 0 0 0 3px rgba(18, 130, 162, 0.2);
    transform: translateY(-2px);
  }
  
  input.invalid {
    border-color: #ff6b6b;
  }
  
  .error-message {
    color: #ff6b6b;
    font-size: 0.875rem;
    margin-top: 0.5rem;
  }
  
  button {
    width: 100%;
    padding: 1rem;
    background: #1282A2;
    color: #FEFCFB;
    border: none;
    border-radius: 0.5rem;
    font-family: 'Source Serif Pro', serif;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }
  
  button:hover {
    background: #034078;
    transform: translateY(-2px);
  }
  
  button:active {
    transform: translateY(0);
  }
  
  /* Animation de chargement */
  button::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.2),
      transparent
    );
    animation: loading 1.5s infinite;
  }
  
  @keyframes loading {
    0% { left: -100%; }
    100% { left: 100%; }
  }
  
  /* Responsive Design */
  @media (max-width: 768px) {
    .min-h-screen {
      padding: 1rem;
    }
  
    .bg-white {
      padding: 1.5rem;
    }
  
    h2 {
      font-size: 1.5rem;
    }
  
    input {
      padding: 0.6rem 0.8rem;
    }
  
    button {
      padding: 0.8rem;
    }
  }
  
  @media (max-width: 480px) {
    .bg-white {
      padding: 1rem;
    }
  
    h2 {
      font-size: 1.25rem;
    }
  
    label {
      font-size: 0.8rem;
    }
  
    input {
      padding: 0.5rem 0.7rem;
    }
  
    .error-message {
      font-size: 0.75rem;
    }
  }
  
  /* Animation d'apparition du formulaire */
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .bg-white {
    animation: fadeIn 0.5s ease-out;
  }
  
  /* Style pour la grille des champs */
  .grid {
    display: grid;
    gap: 1.5rem;
  }
  
  @media (min-width: 640px) {
    .grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  </style>
  