<template>
    <h1>
      Activation de votre compte
    </h1>
  
    active: {{ active }}
    deja: {{ deja }}
    expire: {{ expire }}
    invalid: {{ invalid }}
  
    <div v-if="loading">Activation de votre compte...</div>
    <div v-else>
      <p v-if="success">Votre compte a été activé avec succès!</p>
      <p v-else>Erreur d'activation de votre compte: {{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  import { onMounted, ref } from 'vue';
  import { useRoute } from 'vue-router';
import { useAuthStore } from '../store/authStore';
  
  export default {
    name: 'ActivateAccount',
    setup() {
      const route = useRoute();
      const authStore = useAuthStore();
      const loading = ref(true);
      const success = ref(false);
      const errorMessage = ref(null);
  
      onMounted(() => {
        const { uidb64, token } = route.params;
  
        authStore.activateUser(uidb64, token)
          .then(()=> {
            loading.value = false;
            success.value = true;
          })
          .catch((error) => {
            loading.value = false;
            success.value = false;
            errorMessage.value = error.response?.data?.detail || error.message;
          });
      });
  
      return {
        loading,
        success,
        errorMessage,
      };
    },
  };
  </script>
  