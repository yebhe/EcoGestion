<template>
    <div class="not-found">
      <div class="content">
        <h1>Oups ! Page Introuvable</h1>
        <p>La page que vous recherchez n'existe pas ou a été déplacée.</p>
        <router-link to="/" class="btn-go-home">Retourner à l'accueil</router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NotFound',
  };
  </script>
  
  <style scoped>
  .not-found {
    background-color: rgba(1, 31, 84, 0.7);
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Roboto', sans-serif;
  }
  
  .content {
    text-align: center;
    padding: 30px;
    background-color: rgba(1, 31, 84, 0.9);
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    width: 90%;
    max-width: 600px;
  }
  
  .not-found h1 {
    font-size: 50px;
    color: #ff6347;
    margin-bottom: 20px;
    font-weight: bold;
  }
  
  .not-found p {
    font-size: 20px;
    color: #f9745c;
    margin-bottom: 30px;
  }
  
  .btn-go-home {
    background-color: #ff6347;
    color: white;
    font-size: 18px;
    padding: 12px 25px;
    border-radius: 5px;
    text-decoration: none;
    transition: background-color 0.3s ease, transform 0.2s ease;
  }
  
  .btn-go-home:hover {
    background-color: #ff4500;
    transform: scale(1.1);
  }
  
  .btn-go-home:active {
    background-color: #d84b28;
  }
  
  </style>
  