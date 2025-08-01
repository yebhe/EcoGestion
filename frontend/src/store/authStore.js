import { defineStore } from "pinia";
import axios from "axios";
import { toast } from "vue3-toastify";
import Swal from "sweetalert2";
import router from "../router";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false,
    userRole: null,
    inactivityTimer: null,
  }),
  actions: {
    initializeAuth() {
      const accessToken = localStorage.getItem("accessToken");
      const refreshToken = localStorage.getItem("refreshToken");
      const userRole = localStorage.getItem("userRole");

      if (accessToken && refreshToken && userRole) {
        this.accessToken = accessToken;
        this.refreshToken = refreshToken;
        this.userRole = userRole;
        this.isAuthenticated = true;
        this.setAuthHeaders();

        this.getUserProfile()
          .then(() => {
            this.startInactivityTimer();
          })
          .catch(async (error) => {
            console.error("Error retrieving profile:", error.message);
            // Tentative de refresh du token avant de réinitialiser l'auth
            try {
              await this.refreshAccessToken();
              await this.getUserProfile();
              this.startInactivityTimer();
            } catch (refreshError) {
              console.error("Failed to refresh token:", refreshError);
              this.resetAuth();
            }
          });
      } else {
        this.resetAuth();
      }
    },

    startInactivityTimer() {
      this.stopInactivityTimer();
      this.inactivityTimer = setTimeout(() => {
        this.resetAuth();
        toast("Votre session a expiré après plusieurs minutes d'inactivité", {
          theme: "auto",
          type: "info",
        });
      }, 20 * 60 * 1000);
    },

    resetInactivityTimer() {
      this.startInactivityTimer();
    },

    stopInactivityTimer() {
      if (this.inactivityTimer) {
        clearTimeout(this.inactivityTimer);
        this.inactivityTimer = null;
      }
    },

    logout() {
      this.resetAuth();
      router.push("/login").then(() => {
        toast("Vous êtes déconnecté", {
          theme: "auto",
          type: "info",
        });
      });
    },

    resetAuth() {
      this.accessToken = null;
      this.refreshToken = null;
      this.user = null;
      this.userRole = null;
      this.isAuthenticated = false;
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      localStorage.removeItem("userRole");
      this.stopInactivityTimer();
      delete axios.defaults.headers.common["Authorization"];
    },

    setAuthHeaders() {
      if (this.accessToken) {
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.accessToken}`;
      }
    },

    async getUserProfile() {
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_APP_BASE_URL_API}/user/user/me/`,
          {
            headers: {
              Authorization: `Bearer ${this.accessToken}`,
            },
          }
        );
        this.user = response.data;
        this.userRole = this.user?.is_superuser ? "admin" : this.user.user_type;
        localStorage.setItem("userRole", this.userRole);
        return response.data;
      } catch (error) {
        console.error(
          "Erreur lors de la récupération du profil utilisateur:",
          error.message
        );
        if (error.response?.status === 401) {
          // Si le token est expiré, on peut essayer de le rafraîchir
          try {
            await this.refreshAccessToken();
            // Réessayer après rafraîchissement du token
            return this.getUserProfile();
          } catch (refreshError) {
            this.resetAuth();
          }
        } else {
          this.resetAuth();
        }
        throw error;
      }
    },

    async register(
      username,
      email,
      password,
      firstName,
      lastName,
      phone_number,
      user_type = "client"
    ) {
      try {
        const response = await axios.post(
          `${import.meta.env.VITE_APP_BASE_URL_API}/user/register/`,
          {
            username,
            email,
            password,
            first_name: firstName,
            last_name: lastName,
            phone_number,
            user_type,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        if (response.status === 201) {
          console.log("status crée", response);
          router.push("/login").then(() => {
            toast(
              "Inscription réussie. Veuillez activer votre compte en utilisant le mail reçu.",
              {
                theme: "auto",
                type: "success",
              }
            );
          });
          return { success: true, message: "Inscription réussie" };
        }
      } catch (error) {
        console.log(
          "Error during registration:",
          error.response?.data || error.message
        );

        if (error.response?.data) {
          if (error.response.data.username) {
            toast(`Ce nom d'utilisateur est déjà pris, utilisez un autre`, {
              theme: "auto",
              type: "error",
            });
          }
          if (error.response.data.email) {
            toast(`Cet email existe déjà, utilisez un autre`, {
              theme: "auto",
              type: "error",
            });
          }
          if (error.response.data.password) {
            toast(
              `Le mot de passe est trop semblable au nom d'utilisateur, veillez à créer un mot de passe plus sécurisé`,
              {
                theme: "auto",
                type: "error",
              }
            );
          }
        } else {
          toast("Une erreur s'est produite lors de l'inscription.", {
            theme: "auto",
            type: "error",
          });
        }

        return {
          success: false,
          message: error.response?.data || error.message,
        };
      }
    },

    async login(email, password) {
      try {
        this.resetAuth();

        const response = await axios.post(
          `${import.meta.env.VITE_APP_BASE_URL_API}/user/login/`,
          {
            email,
            password,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        if (response.data?.access && response.data?.refresh) {
          const { access, refresh, user } = response.data;

          this.accessToken = access;
          this.refreshToken = refresh;
          this.isAuthenticated = true;
          this.user = user;
          this.userRole = user?.is_superuser ? "admin" : this.user.user_type;

          localStorage.setItem("accessToken", access);
          localStorage.setItem("refreshToken", refresh);
          localStorage.setItem("userRole", this.userRole);

          this.setAuthHeaders();
          this.startInactivityTimer();

          const roleRedirectMap = {
            admin: "/admin-dashboard",
            client: "/client-dashboard",
            livreur: "/livreur-dashboard",
            commercant: "/commercant-dashboard",
            prestataire: "/prestataire-dashboard",
          };

          const redirectTo = roleRedirectMap[this.userRole];

          if (redirectTo) {
            router.push(redirectTo).then(() => {
              toast("Connexion réussie", {
                theme: "auto",
                type: "success",
              });
            });
            return { success: true, message: "Connexion réussie" };
          } else {
            // Cas où le rôle est inconnu ou non géré
            toast("Rôle utilisateur non reconnu", {
              theme: "auto",
              type: "error",
            });
            return {
              success: false,
              message: "Rôle non reconnu, redirection échouée",
            };
          }
        }
      } catch (error) {
        if (error.response?.status) {
          if (error.response.status === 403) {
            toast(
              `Votre compte n'a pas encore été approuvé. Veuillez attendre l'approbation.`,
              {
                theme: "auto",
                type: "error",
              }
            );
          } else if (error.response.status === 400) {
            toast("Identifiants invalides", {
              theme: "auto",
              type: "error",
            });
          } else {
            toast("Une erreur s'est produite lors de la connexion.", {
              theme: "auto",
              type: "error",
            });
          }
        } else {
          toast("Impossible de se connecter. Veuillez réessayer.", {
            theme: "auto",
            type: "error",
          });
        }

        return {
          success: false,
          message: error.response?.data || error.message,
        };
      }
    },

    async refreshAccessToken() {
      const refresh = this.refreshToken || localStorage.getItem("refreshToken");

      if (!refresh) {
        console.error("Refresh token manquant");
        this.resetAuth();
        throw new Error("Refresh token manquant");
      }

      try {
        const response = await axios.post(
          `${import.meta.env.VITE_APP_BASE_URL_API}/auth/token/refresh/`,
          {
            refresh,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        const { access } = response.data;

        // Mettre à jour le state et localStorage
        this.accessToken = access;
        localStorage.setItem("accessToken", access);
        this.setAuthHeaders();

        // Redémarrer le timer d'inactivité
        this.startInactivityTimer();

        return access;
      } catch (error) {
        console.error(
          "Échec du renouvellement du token:",
          error.response?.data?.detail || error.message
        );

        // En cas d'échec, nettoyer complètement l'auth
        this.resetAuth();

        // Rediriger vers login si on n'y est pas déjà
        if (router.currentRoute.value.path !== "/login") {
          router.push("/login");
        }

        throw error;
      }
    },

    // Méthode pour vérifier si le token est encore valide
    isTokenValid() {
      if (!this.accessToken) return false;

      try {
        // Décoder le JWT pour vérifier l'expiration (optionnel)
        const payload = JSON.parse(atob(this.accessToken.split(".")[1]));
        const now = Date.now() / 1000;

        // Vérifier si le token expire dans moins de 5 minutes
        return payload.exp && payload.exp > now + 300;
      } catch (error) {
        console.error("Erreur lors de la vérification du token:", error);
        return false;
      }
    },

    async activateUser(uidb64, token) {
      try {
        const response = await axios.get(
          `${
            import.meta.env.VITE_APP_BASE_URL_API
          }/user/activate/${uidb64}/${token}/`
        );

        console.log("Response:", response.data);
        if (response.data?.detail) {
          Swal.fire({
            icon: "success",
            title: "Activation réussie",
            text: response.data.detail,
          });
          router.push("/login");
        }
      } catch (error) {
        console.error("Activation error:", error.response?.data);
        if (error.response?.data) {
          if (error.response.data.detail) {
            const errorMessage = error.response.data.detail;
            const isAlreadyActive = errorMessage.includes("déjà activé");

            Swal.fire({
              icon: isAlreadyActive ? "info" : "error",
              title: isAlreadyActive
                ? "Compte déjà activé"
                : "Erreur d'activation",
              text: errorMessage,
            });

            router.push("/login");
          }
        } else {
          Swal.fire({
            icon: "error",
            title: "Erreur",
            text: "Une erreur s'est produite lors de l'activation du compte.",
          });
          router.push("/login");
        }
      }
    },
  },
  persist: true,
});
