<template>
    <div class="dashboard-container">
      <div class="dashboard-card">
        <div class="speedometer">
          <div class="speedometer-dial"></div>
          <div class="speedometer-center"></div>
        </div>
        <br>
        <div class="content-wrapper">
          <h2 class="dashboard-title">Tableau de bord</h2>
  
          <div class="button-group">
            <router-link class="dashboard-btn update-profile" to="/update-profile">
              <span class="btn-icon">🔧</span>
              Modifier votre profil
            </router-link>
            <router-link class="dashboard-btn update-password" to="/update-password">
              <span class="btn-icon">🔐</span>
              Modifier votre mot de passe
            </router-link>
          </div>
  
          <div class="welcome-section" v-if="user">
            <h4 class="welcome-text">Bienvenue sur votre tableau de bord, {{ user.username }}!</h4>
          </div>
  
          <div class="user-info" v-if="user">
            <div class="info-card">
              <span class="info-icon">👤</span>
              <p><strong>Prénom:</strong> {{ user.first_name }}</p>
            </div>
  
            <div class="info-card">
              <span class="info-icon">📋</span>
              <p><strong>Nom:</strong> {{ user.last_name }}</p>
            </div>
  
            <div class="info-card">
              <span class="info-icon">✉️</span>
              <p><strong>Email:</strong> {{ user.email }}</p>
            </div>
  
            <div class="info-card">
              <span class="info-icon">📱</span>
              <p><strong>Numéro de téléphone:</strong> {{ user.phone_number }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  // Script reste identique
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
  
  .dashboard-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #001F54, #034078);
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Source Serif Pro', serif;
    padding: 20px;
    perspective: 1000px;
  }
  
  .dashboard-card {
    background: rgba(254, 252, 251, 0.95);
    border-radius: 20px;
    margin-top: 75px;
    padding: 2rem;
    width: 100%;
    max-width: 800px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
    position: relative;
    transform-style: preserve-3d;
    animation: cardEntry 1s ease-out;
  }
  
  .speedometer {
    position: absolute;
    top: -50px;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 100px;
    background: #0A1128;
    border-radius: 50%;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  }
  
  .speedometer-dial {
    position: absolute;
    width: 4px;
    height: 40px;
    background: #1282A2;
    left: 48px;
    bottom: 50px;
    transform-origin: bottom;
    animation: revDial 2s ease-in-out infinite;
  }
  
  .speedometer-center {
    position: absolute;
    width: 20px;
    height: 20px;
    background: #1282A2;
    border-radius: 50%;
    left: 40px;
    bottom: 40px;
  }
  
  .content-wrapper {
    padding-top: 40px;
  }
  
  .dashboard-title {
    color: #0A1128;
    text-align: center;
    margin-bottom: 2rem;
    font-size: 2.5rem;
    text-transform: uppercase;
    letter-spacing: 2px;
  }
  
  .button-group {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .dashboard-btn {
    background: #1282A2;
    color: white;
    padding: 0.8rem 1.5rem;
    border-radius: 30px;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
  }
  
  .dashboard-btn:hover {
    background: #034078;
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  }
  
  .btn-icon {
    font-size: 1.2rem;
  }
  
  .welcome-section {
    text-align: center;
    margin-bottom: 2rem;
    color: #034078;
    animation: slideIn 0.5s ease-out;
  }
  
  .user-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
  }
  
  .info-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    animation: fadeIn 0.5s ease-out;
  }
  
  .info-card:hover {
    transform: translateY(-5px);
  }
  
  .info-icon {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    display: block;
  }
  
  @keyframes cardEntry {
    from {
      opacity: 0;
      transform: translateY(30px) rotateX(10deg);
    }
    to {
      opacity: 1;
      transform: translateY(0) rotateX(0);
    }
  }
  
  @keyframes revDial {
    0% { transform: rotate(-90deg); }
    50% { transform: rotate(90deg); }
    100% { transform: rotate(-90deg); }
  }
  
  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateX(-30px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: scale(0.9);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
  
  @media (max-width: 768px) {
    .dashboard-card {
      margin-top: 60px;
    }
  
    .button-group {
      flex-direction: column;
      align-items: stretch;
    }
  
    .dashboard-btn {
      width: 100%;
      justify-content: center;
    }
  
    .user-info {
      grid-template-columns: 1fr;
    }
  }
  
  /* Animation for hover effects */
  .info-card p strong {
    color: #034078;
    transition: color 0.3s ease;
  }
  
  .info-card:hover p strong {
    color: #1282A2;
  }
  
  /* Additional car-themed animations */
  .dashboard-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #1282A2, #034078, #1282A2);
    border-radius: 20px 20px 0 0;
    animation: gradient 3s linear infinite;
    background-size: 200% 100%;
  }
  
  @keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }
  </style>
  