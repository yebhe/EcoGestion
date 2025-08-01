import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "vue3-toastify/dist/index.css";
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import axios from 'axios';
import { useAuthStore } from './store/authStore';

const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
app.use(pinia);
app.use(router);

const authStore = useAuthStore();
authStore.initializeAuth();

// Fonction pour configurer l'intercepteur une fois le store disponible
function setupAxiosInterceptor() {
  axios.interceptors.response.use(
    response => response,
    async error => {
      if (error.response?.status === 401 && !error.config.url?.includes('/auth/token/refresh/')) {
        try {
          // Import dynamique pour éviter les références circulaires
          const { useAuthStore } = await import('./store/authStore');
          const authStore = useAuthStore();
          
          if (authStore && authStore.refreshToken && authStore.isAuthenticated) {
            try {
              await authStore.refreshAccessToken();
              
              // Recréer la requête avec le nouveau token
              const originalRequest = error.config;
              originalRequest.headers['Authorization'] = `Bearer ${authStore.accessToken}`;
              return axios(originalRequest);
            } catch (refreshError) {
              console.error('Échec du refresh token:', refreshError);
              authStore.logout();
              return Promise.reject(refreshError);
            }
          }
        } catch (storeError) {
          console.error('Erreur lors de l\'accès au store:', storeError);
        }
      }
      return Promise.reject(error);
    }
  );
}

// Monter l'application et configurer l'intercepteur après
app.mount('#app');

// Configurer l'intercepteur après que tout soit initialisé
setupAxiosInterceptor();