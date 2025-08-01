<template>
    <br>
    <br>
    <div class="dash">
    <br>
    <br>
    <router-link class="btn btn-info my-3" to="/update-profile">Modifier votre profile</router-link>
    <router-link class="btn btn-info" to="/update-password">Modifier votre mot de passe</router-link>
    <h2>Tableau de bord</h2>
    <h4 v-if="user">Bienvenue sur votre tableau de bord, {{ user.username }}!</h4>
    <div v-if="user">
      <p><strong>Prénom:</strong> {{ user.first_name }}</p>
      <p><strong>Nom:</strong> {{ user.last_name }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>Numéro de téléphone:</strong> {{ user.phone_number }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../../store/authStore';


const user = ref(null);
const authStore = useAuthStore();
const token = localStorage.getItem('token');
if (token) {
  authStore.setToken(token);
}

const fetchUserProfile = async () => {
  try {
    user.value = await authStore.getUserProfile();
    console.log('Données de l\'utilisateur:', user.value);
  } catch (error) {
    console.error('Échec de la récupération des données de l\'utilisateur:', error);
  }
};


onMounted(() => {
  fetchUserProfile();
});
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+Pro:wght@400;600;700&display=swap');

.dash {
  min-height: 100vh;
  background: #FEFCFB;
  font-family: 'Source Serif Pro', serif;
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

/* Animation d'un véhicule qui traverse l'écran */
.dash::before {
  content: '🚗';
  position: absolute;
  font-size: 2rem;
  top: 10px;
  left: -50px;
  animation: driveby 15s linear infinite;
  opacity: 0.3;
}

@keyframes driveby {
  from {
    transform: translateX(-50px) rotate(0deg);
  }
  to {
    transform: translateX(calc(100vw + 50px)) rotate(0deg);
  }
}

h2 {
  color: #0A1128;
  font-size: 2.8rem;
  margin-bottom: 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

h2::after {
  content: '🔧';
  position: absolute;
  right: 20px;
  animation: wrench 3s ease-in-out infinite;
}

@keyframes wrench {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(20deg); }
  75% { transform: rotate(-20deg); }
}

h4 {
  color: #034078;
  font-size: 1.8rem;
  margin-bottom: 2rem;
  text-align: center;
}

.dash > div {
  background: #001F54;
  padding: 2.5rem;
  border-radius: 15px;
  box-shadow: 0 0 30px rgba(18, 130, 162, 0.2);
  color: #FEFCFB;
  max-width: 800px;
  margin: 0 auto;
  transform-style: preserve-3d;
  transition: transform 0.3s ease;
}

.dash > div:hover {
  transform: translateY(-5px) rotateX(5deg);
}

p {
  font-size: 1.2rem;
  margin: 1.5rem 0;
  padding: 1rem;
  border-radius: 8px;
  background: rgba(254, 252, 251, 0.05);
  transition: all 0.3s ease;
  position: relative;
}

p:hover {
  background: rgba(18, 130, 162, 0.1);
  transform: translateX(10px);
}

strong {
  color: #1282A2;
  margin-right: 1rem;
}

.btn {
  display: inline-block;
  padding: 1rem 2rem;
  margin: 1rem;
  background: #1282A2;
  color: #FEFCFB;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s ease;
  border: none;
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '🔄';
  position: absolute;
  left: -30px;
  opacity: 0;
  transition: all 0.3s ease;
}

.btn:hover {
  background: #034078;
  padding-left: 3rem;
}

.btn:hover::before {
  left: 1rem;
  opacity: 1;
}

/* Animation des roues qui tournent */
@keyframes wheelSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.dash::after {
  content: '⚙️';
  position: fixed;
  bottom: 20px;
  right: 20px;
  font-size: 2rem;
  animation: wheelSpin 4s linear infinite;
  opacity: 0.3;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dash {
    padding: 1rem;
  }

  h2 {
    font-size: 2rem;
  }

  h4 {
    font-size: 1.4rem;
  }

  .dash > div {
    padding: 1.5rem;
  }

  .btn {
    display: block;
    margin: 1rem 0;
    text-align: center;
  }
}

</style>
