<template>
    <div>
      <h1>Activation du compte</h1>
      <p v-if="message" style="display: none;">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import Swal from 'sweetalert2';
import router from '../router';
  
  export default {
    name: 'ActivationResult',
    data() {
      return {
        message: null,
      };
    },
    mounted() {
      const urlParams = new URLSearchParams(window.location.search);
      this.message = urlParams.get('message');
  
      if (this.message) {
        this.displaySwalAlert(this.message);
      }
    },
    methods: {
      displaySwalAlert(message) {
        let title = '';
        let icon = '';
  
        if (message.includes('succès')) {
          title = 'Activation Réussie';
          icon = 'success';
        } else if (message.includes('déjà')) {
          title = 'Information';
          icon = 'info';
        } else if (message.includes('invalide') || message.includes('expiré')) {
          title = 'Erreur';
          icon = 'error';
        } else {
          title = 'Attention';
          icon = 'warning';
        }
        router.push('/');
        Swal.fire({
          title: title,
          text: message,
          icon: icon,
          confirmButtonText: 'OK',
        });
      },
    },
  };
  </script>
  
  <style scoped>
  </style>
  