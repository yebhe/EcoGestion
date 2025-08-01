<template>
  <div class="planning-container">
    <div class="planning-card">
      <h2 class="planning-title">Gestion de mon planning</h2>
      
      <div class="planning-actions">
        <button class="action-btn primary-btn" @click="showAddModalOptimized">
          <span class="btn-icon">➕</span>
          <span class="btn-text">Ajouter une disponibilité</span>
        </button>
        
        <div class="view-toggle">
          <button class="toggle-btn" :class="{ active: currentView === 'calendar' }" @click="currentView = 'calendar'">
            <span class="toggle-icon">📅</span>
            <span>Calendrier</span>
          </button>
          <button class="toggle-btn" :class="{ active: currentView === 'list' }" @click="currentView = 'list'">
            <span class="toggle-icon">📋</span>
            <span>Liste</span>
          </button>
        </div>
      </div>
      
      <!-- Calendrier -->
      <div v-if="currentView === 'calendar'" class="calendar-view">
        <div class="calendar-header">
          <button class="nav-btn" @click="previousMonth">
            <span>◀</span>
          </button>
          <h3 class="current-month">{{ formatMonth(currentMonth) }}</h3>
          <button class="nav-btn" @click="nextMonth">
            <span>▶</span>
          </button>
        </div>
        
        <div class="calendar-grid">
          <div class="day-header" v-for="day in weekDays" :key="day">{{ day }}</div>
          <div
            v-for="day in calendarDays"
            :key="day.date"
            class="calendar-day"
            :class="{ 
              'other-month': day.otherMonth, 
              'today': day.isToday,
              'has-availability': day.hasAvailability,
              'selected': isSelectedDay(day)
            }"
            @click="selectDay(day)"
          >
            <span class="day-number">{{ new Date(day.date).getDate() }}</span>
            <div v-if="day.hasAvailability" class="availability-indicator"></div>
          </div>
        </div>
        
        <transition name="slide-fade">
          <div v-if="selectedDay" class="day-details">
            <h4>{{ isMobile ? 'Disponibilités' : 'Disponibilités du ' + formatDate(selectedDay.date) }}</h4>
            <div v-if="selectedDayAvailabilities.length === 0" class="no-data">
              Aucune disponibilité pour cette date.
            </div>
            <div v-else class="availability-list">
              <div 
                v-for="(availability, index) in selectedDayAvailabilities" 
                :key="index" 
                class="availability-item"
                :class="{ 'mobile-item': isMobile }"
                :style="{ animationDelay: index * 0.1 + 's' }"
              >
                <div class="availability-time">
                  <span>{{ formatTime(availability.date_debut) }} - {{ formatTime(availability.date_fin) }}</span>
                  <span class="availability-duration">{{ calculateDuration(availability.date_debut, availability.date_fin) }}</span>
                </div>
                <div class="availability-actions">
                  <button class="icon-btn edit-btn" @click="editAvailabilityOptimized(availability)">
                    <span class="btn-hover-text">Modifier</span>
                    <span class="btn-icon">✏️</span>
                  </button>
                  <button class="icon-btn delete-btn" @click="confirmDeleteAvailability(availability)">
                    <span class="btn-hover-text">Supprimer</span>
                    <span class="btn-icon">🗑️</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </transition>
      </div>
      
      <!-- Vue liste -->
      <div v-else-if="currentView === 'list'" class="list-view">
        <div class="list-header">
          <h3>Mes disponibilités à venir</h3>
          <div class="filter-controls">
            <select v-model="filterPeriod" class="filter-select">
              <option value="upcoming">À venir</option>
              <option value="week">Cette semaine</option>
              <option value="month">Ce mois</option>
              <option value="all">Toutes</option>
            </select>
          </div>
        </div>
        
        <transition name="fade">
          <div v-if="filteredAvailabilities.length === 0" class="no-data">
            <div class="empty-state">
              <div class="empty-icon">📆</div>
              <h4>Aucune disponibilité trouvée</h4>
              <p>Vous n'avez pas encore défini de disponibilités pour cette période.</p>
              <button class="action-btn primary-btn add-first-btn" @click="showAddModalOptimized">
                <span class="btn-icon">➕</span>
                <span class="btn-text">Ajouter ma première disponibilité</span>
              </button>
            </div>
          </div>
        </transition>
        
        <transition-group name="list" tag="div" class="availability-list-container">
          <div v-for="(group, date) in groupedAvailabilities" :key="date" class="availability-group">
            <div class="group-date">{{ formatDate(date) }}</div>
            <div v-for="(availability, index) in group" :key="availability.id" 
                 class="availability-item" :class="{ 'mobile-item': isMobile }">
              <div class="availability-time">
                <span>{{ formatTime(availability.date_debut) }} - {{ formatTime(availability.date_fin) }}</span>
                <span class="availability-duration">{{ calculateDuration(availability.date_debut, availability.date_fin) }}</span>
              </div>
              <div class="availability-actions">
                <button class="icon-btn edit-btn" @click="editAvailabilityOptimized(availability)">
                  <span class="btn-hover-text">Modifier</span>
                  <span class="btn-icon">✏️</span>
                </button>
                <button class="icon-btn delete-btn" @click="confirmDeleteAvailability(availability)">
                  <span class="btn-hover-text">Supprimer</span>
                  <span class="btn-icon">🗑️</span>
                </button>
              </div>
            </div>
          </div>
        </transition-group>
      </div>
      
      <!-- Modal d'ajout/édition -->
      <transition name="modal">
        <div v-if="showAddModal" class="modal-backdrop" @click.self="closeModal">
          <div class="modal-container">
            <div class="modal-header">
              <h4>{{ editMode ? 'Modifier une disponibilité' : 'Ajouter une disponibilité' }}</h4>
              <button class="close-btn" @click="closeModal">×</button>
            </div>
            <div class="modal-body">
              <div class="form-group">
                <label for="date">Date</label>
                <input type="date" id="date" v-model="newAvailability.date" class="form-input" :min="today" required>
              </div>
              <div class="form-row" :class="{ 'form-column': isMobile }">
                <div class="form-group">
                  <label for="start-time">Heure de début</label>
                  <input type="time" id="start-time" v-model="newAvailability.startTime" class="form-input" required>
                </div>
                <div class="form-group">
                  <label for="end-time">Heure de fin</label>
                  <input type="time" id="end-time" v-model="newAvailability.endTime" class="form-input" required>
                </div>
              </div>
              <span v-if="timeError" class="error-message">{{ timeError }}</span>
              
              <div class="time-info">
                <div class="time-icon">⏱️</div>
                <p>Définissez vos disponibilités pour recevoir des demandes de livraison pendant ces heures.</p>
              </div>
            </div>
            <div class="modal-footer">
              <button class="action-btn secondary-btn" @click="closeModal">Annuler</button>
              <button class="action-btn primary-btn" @click="saveAvailability" :disabled="!!timeError">
                {{ editMode ? 'Modifier' : 'Ajouter' }}
              </button>
            </div>
          </div>
        </div>
      </transition>
      
      <!-- Modal de confirmation de suppression -->
      <transition name="modal">
        <div v-if="showDeleteModal" class="modal-backdrop">
          <div class="modal-container delete-modal">
            <div class="modal-header">
              <h4>Confirmer la suppression</h4>
              <button class="close-btn" @click="showDeleteModal = false">×</button>
            </div>
            <div class="modal-body">
              <div class="delete-warning">
                <div class="warning-icon">⚠️</div>
                <p>Êtes-vous sûr de vouloir supprimer cette disponibilité ?</p>
              </div>
              <div class="availability-details">
                <p><strong>Date :</strong> {{ formatDate(availabilityToDelete.date_debut) }}</p>
                <p><strong>Horaire :</strong> {{ formatTime(availabilityToDelete.date_debut) }} - {{ formatTime(availabilityToDelete.date_fin) }}</p>
              </div>
            </div>
            <div class="modal-footer">
              <button class="action-btn secondary-btn" @click="showDeleteModal = false">Annuler</button>
              <button class="action-btn danger-btn" @click="deleteAvailability">
                <span class="btn-icon">🗑️</span>
                <span>Supprimer</span>
              </button>
            </div>
          </div>
        </div>
      </transition>
      
      <!-- Toast notification -->
      <transition name="toast">
        <div v-if="showToast" class="toast-notification" :class="[toastType, {'toast-mobile': isMobile}]">
          <div class="toast-icon">{{ toastIcon }}</div>
          <div class="toast-message">{{ toastMessage }}</div>
          <button class="toast-close" @click="showToast = false">×</button>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue';
import axios from 'axios';

export default {
  name: 'PlanningView',
  setup() {
    // État
    const availabilities = ref([]);
    const currentView = ref('calendar');
    const currentMonth = ref(new Date());
    const selectedDay = ref(null);
    const showAddModal = ref(false);
    const showDeleteModal = ref(false);
    const editMode = ref(false);
    const availabilityToEdit = ref(null);
    const availabilityToDelete = ref({});
    const filterPeriod = ref('upcoming');
    const timeError = ref('');
    const showToast = ref(false);
    const toastMessage = ref('');
    const toastType = ref('');
    const toastIcon = ref('');
    
    const today = new Date().toISOString().split('T')[0];
    
    const newAvailability = ref({
      date: today,
      startTime: '09:00',
      endTime: '18:00'
    });
    
    // Détecter si on est sur mobile
    const isMobile = computed(() => {
      return window.innerWidth <= 768;
    });
    
    // Jours de la semaine
    const weekDays = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];
    
    // Fonctions auxiliaires pour les dates
    const formatDate = (date) => {
      if (!date) return '';
      const options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
      return new Date(date).toLocaleDateString('fr-FR', options);
    };
    
    const formatTime = (datetime) => {
      if (!datetime) return '';
      const date = new Date(datetime);
      // Version plus compacte sur mobile
      return date.toLocaleTimeString('fr-FR', { 
        hour: '2-digit', 
        minute: '2-digit', 
        hour12: false // Format 24h explicite
      });
    };
    
    const formatMonth = (date) => {
      const options = { month: 'long', year: 'numeric' };
      return date.toLocaleDateString('fr-FR', options);
    };
    
    const calculateDuration = (start, end) => {
      if (!start || !end) return '';
      const startDate = new Date(start);
      const endDate = new Date(end);
      const diff = Math.abs(endDate - startDate);
      const hours = Math.floor(diff / 3600000);
      const minutes = Math.floor((diff % 3600000) / 60000);
      
      if (hours === 0) {
        return `${minutes} min`;
      } else if (minutes === 0) {
        return `${hours} h`;
      } else {
        return `${hours} h ${minutes} min`;
      }
    };
    
    // Vérifier si un jour est le jour sélectionné
    const isSelectedDay = (day) => {
      if (!selectedDay.value || !day) return false;
      return day.date.toDateString() === selectedDay.value.date.toDateString();
    };
    
    // Fonctions pour le calendrier
    const calendarDays = computed(() => {
      const year = currentMonth.value.getFullYear();
      const month = currentMonth.value.getMonth();
      
      const firstDayOfMonth = new Date(year, month, 1);
      const lastDayOfMonth = new Date(year, month + 1, 0);
      
      // Calculer le premier jour de la semaine à afficher (lundi précédent le 1er du mois)
      let firstCalendarDay = new Date(firstDayOfMonth);
      const dayOfWeek = firstCalendarDay.getDay() || 7; // 0 (dimanche) => 7 pour l'ordre européen
      if (dayOfWeek > 1) {
        firstCalendarDay.setDate(firstCalendarDay.getDate() - (dayOfWeek - 1));
      }
      
      // Calculer le dernier jour à afficher (dimanche suivant le dernier jour du mois)
      let lastCalendarDay = new Date(lastDayOfMonth);
      const lastDayOfWeek = lastCalendarDay.getDay() || 7;
      if (lastDayOfWeek < 7) {
        lastCalendarDay.setDate(lastCalendarDay.getDate() + (7 - lastDayOfWeek));
      }
      
      // Créer le tableau des jours du calendrier
      const days = [];
      let currentDate = new Date(firstCalendarDay);
      
      while (currentDate <= lastCalendarDay) {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        days.push({
          date: new Date(currentDate),
          otherMonth: currentDate.getMonth() !== month,
          isToday: currentDate.getTime() === today.getTime(),
          hasAvailability: hasAvailabilityForDay(currentDate)
        });
        
        currentDate.setDate(currentDate.getDate() + 1);
      }
      
      return days;
    });
    
    const hasAvailabilityForDay = (date) => {
      const formattedDate = date.toISOString().split('T')[0];
      return availabilities.value.some(avail => {
        const availDate = new Date(avail.date_debut).toISOString().split('T')[0];
        return availDate === formattedDate;
      });
    };
    
    const selectedDayAvailabilities = computed(() => {
      if (!selectedDay.value) return [];
      
      const selectedDateStr = selectedDay.value.date.toISOString().split('T')[0];
      return availabilities.value.filter(avail => {
        const availDate = new Date(avail.date_debut).toISOString().split('T')[0];
        return availDate === selectedDateStr;
      }).sort((a, b) => new Date(a.date_debut) - new Date(b.date_debut));
    });
    
    const nextMonth = () => {
      currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() + 1, 1);
    };
    
    const previousMonth = () => {
      currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() - 1, 1);
    };
    
    const selectDay = (day) => {
      selectedDay.value = day;
    };
    
    // Adapter la vue pour mobile
    const adaptViewForMobile = () => {
      // Passer automatiquement à la vue liste sur les petits écrans en mode portrait
      if (isMobile.value && window.innerHeight > window.innerWidth) {
        currentView.value = 'list';
      }
    };
    
    // Afficher un toast de notification
    const showToastMessage = (message, type = 'success') => {
      toastMessage.value = message;
      toastType.value = type;
      
      if (type === 'success') {
        toastIcon.value = '✅';
      } else if (type === 'error') {
        toastIcon.value = '❌';
      } else if (type === 'info') {
        toastIcon.value = 'ℹ️';
      }
      
      showToast.value = true;
      
      // Masquer le toast après 3 secondes
      setTimeout(() => {
        showToast.value = false;
      }, 3000);
    };
    
    // Fonctions pour filtrer les disponibilités
    const filteredAvailabilities = computed(() => {
      const now = new Date();
      
      // Définir les filtres par période
      switch (filterPeriod.value) {
        case 'upcoming':
          return availabilities.value.filter(avail => new Date(avail.date_debut) >= now);
        
        case 'week': {
          const startOfWeek = new Date(now);
          startOfWeek.setDate(now.getDate() - now.getDay() + 1); // Lundi de la semaine en cours
          startOfWeek.setHours(0, 0, 0, 0);
          
          const endOfWeek = new Date(startOfWeek);
          endOfWeek.setDate(startOfWeek.getDate() + 6); // Dimanche
          endOfWeek.setHours(23, 59, 59, 999);
          
          return availabilities.value.filter(avail => {
            const availDate = new Date(avail.date_debut);
            return availDate >= startOfWeek && availDate <= endOfWeek;
          });
        }
        
        case 'month': {
          const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
          const endOfMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59, 999);
          
          return availabilities.value.filter(avail => {
            const availDate = new Date(avail.date_debut);
            return availDate >= startOfMonth && availDate <= endOfMonth;
          });
        }
        
        case 'all':
        default:
          return availabilities.value;
      }
    });
    
    // Grouper les disponibilités par date
    const groupedAvailabilities = computed(() => {
      const groups = {};
      
      filteredAvailabilities.value.forEach(avail => {
        const date = new Date(avail.date_debut).toISOString().split('T')[0];
        if (!groups[date]) {
          groups[date] = [];
        }
        groups[date].push(avail);
      });
      
      // Trier les groupes par date
      const sortedGroups = {};
      Object.keys(groups).sort().forEach(date => {
        sortedGroups[date] = groups[date];
      });
      
      return sortedGroups;
    });
    
    // Actions sur les disponibilités
    const fetchAvailabilities = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/disponibilites/`);
        availabilities.value = response.data;
      } catch (error) {
        console.error('Erreur lors de la récupération des disponibilités:', error);
        showToastMessage('Erreur lors du chargement des disponibilités', 'error');
      }
    };
    
    const validateTimes = () => {
      timeError.value = '';
      
      const startDateTime = new Date(`${newAvailability.value.date}T${newAvailability.value.startTime}:00`);
      const endDateTime = new Date(`${newAvailability.value.date}T${newAvailability.value.endTime}:00`);
      const now = new Date();
      
      // Vérifier que l'heure de début est dans le futur
      if (startDateTime < now) {
        timeError.value = "L'heure de début doit être dans le futur";
        return false;
      }
      
      // Vérifier que l'heure de fin est après l'heure de début
      if (startDateTime >= endDateTime) {
        timeError.value = "L'heure de fin doit être après l'heure de début";
        return false;
      }
      
      // Vérifier si la disponibilité chevauche une autre
      if (!editMode.value || (editMode.value && availabilityToEdit.value)) {
        const existingAvailabilities = availabilities.value.filter(avail => {
          if (editMode.value && availabilityToEdit.value && avail.id === availabilityToEdit.value.id) {
            return false;
          }
          
          const availStartDate = new Date(avail.date_debut);
          const availEndDate = new Date(avail.date_fin);
          const availDateStr = availStartDate.toISOString().split('T')[0];
          
          return availDateStr === newAvailability.value.date && 
                ((startDateTime >= availStartDate && startDateTime < availEndDate) ||
                 (endDateTime > availStartDate && endDateTime <= availEndDate) ||
                 (startDateTime <= availStartDate && endDateTime >= availEndDate));
        });
        
        if (existingAvailabilities.length > 0) {
          timeError.value = "Cette plage horaire chevauche une disponibilité existante";
          return false;
        }
      }
      
      return true;
    };
    
    const saveAvailability = async () => {
      if (!validateTimes()) return;
    
      try {
        const data = {
          date_debut: `${newAvailability.value.date}T${newAvailability.value.startTime}:00`,
          date_fin: `${newAvailability.value.date}T${newAvailability.value.endTime}:00`
        };
    
        let response;
        if (editMode.value && availabilityToEdit.value) {
          response = await axios.put(
            `${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/disponibilites/${availabilityToEdit.value.id}/`,
            data
          );
          showToastMessage('Disponibilité modifiée avec succès', 'success');
        } else {
          response = await axios.post(
            `${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/disponibilites/`,
            data
          );
          showToastMessage('Disponibilité ajoutée avec succès', 'success');
        }
    
        await fetchAvailabilities();
        closeModal();
      } catch (error) {
        console.error('Erreur lors de la sauvegarde de la disponibilité:', error);
        showToastMessage('Erreur lors de l\'enregistrement', 'error');
      }
    };
    
    // Méthode optimisée pour l'ouverture du modal
    const openModalMobile = () => {
      showAddModal.value = true;
      
      // Empêcher le scroll de la page sous le modal sur mobile
      if (isMobile.value) {
        document.body.style.overflow = 'hidden';
        
        // Défiler automatiquement en haut du modal après son ouverture
        setTimeout(() => {
          const modalBody = document.querySelector('.modal-body');
          if (modalBody) modalBody.scrollTop = 0;
        }, 100);
      }
    };
    
    // Utiliser cette méthode au lieu de showAddModal = true
    const showAddModalOptimized = () => {
      // Réinitialiser les valeurs par défaut
      newAvailability.value = {
        date: today,
        startTime: '09:00',
        endTime: '18:00'
      };
      openModalMobile();
    };
    
    // Méthode optimisée pour l'édition
    const editAvailabilityOptimized = (availability) => {
      availabilityToEdit.value = availability;
      editMode.value = true;
      
      const startDate = new Date(availability.date_debut);
      const endDate = new Date(availability.date_fin);
      
      newAvailability.value = {
        date: startDate.toISOString().split('T')[0],
        startTime: startDate.toTimeString().substring(0, 5),
        endTime: endDate.toTimeString().substring(0, 5)
      };
      
      openModalMobile();
    };
    
    const confirmDeleteAvailability = (availability) => {
      availabilityToDelete.value = availability;
      showDeleteModal.value = true;
    };
    
    const deleteAvailability = async () => {
      try {
        await axios.delete(`${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/disponibilites/${availabilityToDelete.value.id}/`);
        await fetchAvailabilities();
        showDeleteModal.value = false;
        showToastMessage('Disponibilité supprimée avec succès', 'success');
      } catch (error) {
        console.error('Erreur lors de la suppression de la disponibilité:', error);
        showToastMessage('Erreur lors de la suppression', 'error');
      }
    };
    
    const closeModal = () => {
      showAddModal.value = false;
      editMode.value = false;
      availabilityToEdit.value = null;
      timeError.value = '';
      newAvailability.value = {
        date: today,
        startTime: '09:00',
        endTime: '18:00'
      };
      
      // Rétablir le scroll sur mobile
      if (isMobile.value) {
        document.body.style.overflow = 'auto';
      }
    };
    
    // Cycle de vie du composant
    onMounted(() => {
      fetchAvailabilities();
      adaptViewForMobile();
      
      // Écouteur de redimensionnement pour ajuster la vue si nécessaire
      window.addEventListener('resize', adaptViewForMobile);
    });
    
    // Nettoyage des écouteurs à la destruction du composant
    onUnmounted(() => {
      window.removeEventListener('resize', adaptViewForMobile);
    });
    
    // Surveiller les changements de date/heure pour validation
    watch(
      [() => newAvailability.value.date, () => newAvailability.value.startTime, () => newAvailability.value.endTime],
      () => {
        if (newAvailability.value.date && newAvailability.value.startTime && newAvailability.value.endTime) {
          validateTimes();
        }
      }
    );
    
    // Surveiller les changements de vue et de mois pour actualiser les données
    watch([currentView, currentMonth], () => {
      fetchAvailabilities();
    });
    
    return {
      availabilities,
      currentView,
      currentMonth,
      selectedDay,
      showAddModal,
      showDeleteModal,
      editMode,
      availabilityToEdit,
      availabilityToDelete,
      filterPeriod,
      timeError,
      today,
      newAvailability,
      weekDays,
      calendarDays,
      selectedDayAvailabilities,
      filteredAvailabilities,
      groupedAvailabilities,
      showToast,
      toastMessage,
      toastType,
      toastIcon,
      isMobile,
      formatDate,
      formatTime,
      formatMonth,
      calculateDuration,
      isSelectedDay,
      nextMonth,
      previousMonth,
      selectDay,
      validateTimes,
      saveAvailability,
      editAvailabilityOptimized,
      showAddModalOptimized,
      confirmDeleteAvailability,
      deleteAvailability,
      closeModal,
      showToastMessage
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+Pro:wght@400;600;700&display=swap');

.planning-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #001F54, #034078);
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Source Serif Pro', serif;
  padding: 20px;
}

.planning-card {
  background: rgba(254, 252, 251, 0.95);
  border-radius: 20px;
  padding: 2rem;
  width:100%;
  max-width: 900px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  animation: cardEntry 1s ease-out;
  position: relative;
}

.planning-title {
  color: #0A1128;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2.5rem;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.planning-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.action-btn {
  padding: 0.8rem 1.5rem;
  border-radius: 50px;
  border: none;
  font-family: 'Source Serif Pro', serif;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.primary-btn {
  background: #1282A2;
  color: white;
}

.primary-btn:hover {
  background: #034078;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.secondary-btn {
  background: #f0f0f0;
  color: #333;
}

.secondary-btn:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
}

.danger-btn {
  background: #F44336;
  color: white;
}

.danger-btn:hover {
  background: #D32F2F;
  transform: translateY(-2px);
}

.btn-icon {
  font-size: 1.2rem;
}

.view-toggle {
  display: flex;
  background: #f0f0f0;
  border-radius: 50px;
  padding: 0.3rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.toggle-btn {
  background: none;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  font-family: 'Source Serif Pro', serif;
}

.toggle-btn.active {
  background: #1282A2;
  color: white;
}

.toggle-icon {
  font-size: 1.2rem;
}

/* Styles du calendrier */
.calendar-view {
  background: white;
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  animation: fadeIn 0.5s ease-out;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.current-month {
  font-size: 1.5rem;
  margin: 0;
  text-transform: capitalize;
  color: #0A1128;
}

.nav-btn {
  background: #f0f0f0;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background: #1282A2;
  color: white;
  transform: scale(1.1);
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
}

.day-header {
  font-weight: 600;
  padding: 0.5rem;
  color: #0A1128;
}

.calendar-day {
  height: 40px;
  border-radius: 10px;
  background: #f9f9f9;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.calendar-day:hover {
  background: #e9e9e9;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.day-number {
  font-weight: 600;
  color: #0A1128;
}

.other-month {
  opacity: 0.5;
}

.today {
  background: #E3F2FD;
  border: 2px solid #1282A2;
}

.selected {
  background: #e0f7fa;
  border: 2px solid #00acc1;
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.has-availability .availability-indicator {
  position: absolute;
  bottom: 5px;
  right: 5px;
  width: 8px;
  height: 8px;
  background: #4CAF50;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.day-details {
  margin-top: 2rem;
  background: white;
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.day-details h4 {
  color: #0A1128;
  margin-top: 0;
  margin-bottom: 1rem;
  text-transform: capitalize;
}

/* Styles de la vue liste */
.list-view {
  background: white;
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  animation: fadeIn 0.5s ease-out;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.list-header h3 {
  margin: 0;
  color: #0A1128;
}

.filter-select {
  padding: 0.5rem 1rem;
  border-radius: 25px;
  border: 1px solid #ddd;
  font-family: 'Source Serif Pro', serif;
  background-color: #f5f5f5;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-select:focus {
  outline: none;
  border-color: #1282A2;
  box-shadow: 0 0 0 2px rgba(18, 130, 162, 0.2);
}

.availability-list-container {
  max-height: 500px;
  overflow-y: auto;
  padding-right: 5px;
}

.availability-group {
  margin-bottom: 1.5rem;
}

.group-date {
  font-weight: 600;
  color: #0A1128;
  margin-bottom: 0.5rem;
  text-transform: capitalize;
  border-bottom: 2px solid #1282A2;
  padding-bottom: 0.5rem;
}

.availability-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.availability-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
  transition: all 0.3s ease;
  animation: slideIn 0.3s ease-out forwards;
}

.mobile-item {
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
}

.availability-item:hover {
  background: #e9e9e9;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.availability-time {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.availability-duration {
  font-size: 0.9rem;
  color: #666;
}

.availability-actions {
  display: flex;
  gap: 0.5rem;
}

.mobile-item .availability-actions {
  align-self: flex-end;
  margin-top: 0.5rem;
}

.icon-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.3rem;
  border-radius: 50%;
  transition: all 0.3s ease;
  position: relative;
}

.btn-hover-text {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%) scale(0);
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  pointer-events: none;
  transition: transform 0.2s ease;
  white-space: nowrap;
}

.icon-btn:hover .btn-hover-text {
  transform: translateX(-50%) scale(1);
}

.edit-btn:hover {
  background: #E3F2FD;
}

.delete-btn:hover {
  background: #FFEBEE;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem 2rem;
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  animation: bounce 2s infinite;
}

.empty-state h4 {
  color: #0A1128;
  margin: 0 0 0.5rem;
}

.empty-state p {
  color: #666;
  margin: 0 0 1.5rem;
}

.add-first-btn {
  margin-top: 1rem;
}

.no-data {
  padding: 1rem;
  text-align: center;
  color: #666;
  font-style: italic;
}

/* Styles du modal */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-container {
  background: white;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem;
  border-bottom: 1px solid #eee;
  background: #f5f5f5;
}

.modal-header h4 {
  margin: 0;
  color: #0A1128;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  color: #666;
  cursor: pointer;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 1.2rem;
}

.form-group {
  margin-bottom: 1.2rem;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-column {
  flex-direction: column;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #0A1128;
  font-weight: 600;
}

.form-input {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-family: 'Source Serif Pro', serif;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #1282A2;
  box-shadow: 0 0 0 2px rgba(18, 130, 162, 0.2);
}

.error-message {
  color: #F44336;
  font-size: 0.85rem;
  margin-top: 0.3rem;
  display: block;
}

.time-info {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 0.8rem;
  background: #f5f5f5;
  border-radius: 5px;
  margin-top: 1rem;
}

.time-icon {
  font-size: 1.2rem;
}

.time-info p {
  margin: 0;
  font-size: 0.85rem;
  color: #555;
}

.delete-warning {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 1rem;
  background: #FFEBEE;
  border-radius: 5px;
  margin-bottom: 1rem;
}

.warning-icon {
  font-size: 1.5rem;
}

.delete-warning p {
  margin: 0;
  color: #D32F2F;
  font-weight: 500;
}

.availability-details {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 5px;
}

.availability-details p {
  margin: 0.5rem 0;
}

.modal-footer {
  padding: 1rem 1.2rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  background: #f5f5f5;
  border-top: 1px solid #eee;
}

/* Toast notification */
.toast-notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: white;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  min-width: 250px;
  max-width: 350px;
}

.toast-mobile {
  left: 20px;
  right: 20px;
  bottom: 20px;
  min-width: auto;
  max-width: none;
}

.toast-notification.success {
  border-left: 4px solid #4CAF50;
}

.toast-notification.error {
  border-left: 4px solid #F44336;
}

.toast-notification.info {
  border-left: 4px solid #2196F3;
}

.toast-icon {
  font-size: 1.5rem;
}

.toast-message {
  flex: 1;
  font-size: 0.9rem;
}

.toast-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #888;
  cursor: pointer;
}

/* Animations */
@keyframes cardEntry {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.3);
    opacity: 0.7;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-15px);
  }
  60% {
    transform: translateY(-7px);
  }
}

/* Transitions */
.slide-fade-enter-active, .slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from, .slide-fade-leave-to {
  transform: translateY(10px);
  opacity: 0;
}

.modal-enter-active, .modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container, .modal-leave-to .modal-container {
  transform: scale(0.9);
}

.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from, .toast-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.list-enter-active, .list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from, .list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.list-move {
  transition: transform 0.3s ease;
}

/* Responsive design */
@media (max-width: 768px) {
  .planning-container {
    padding: 10px;
    align-items: flex-start;
    min-height: auto;
  }
  
  .planning-card {
    padding: 1rem;
    border-radius: 15px;
    margin: 10px 0;
  }
  
  .planning-title {
    font-size: 1.8rem;
    margin-bottom: 1.2rem;
  }
  
  .planning-actions {
    flex-direction: column;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
  }
  
  .view-toggle {
    width: 100%;
    justify-content: center;
  }
  
  .toggle-btn {
    flex: 1;
    justify-content: center;
  }
  
  .action-btn.primary-btn {
    width: 100%;
    justify-content: center;
  }
  
  /* Ajustements du calendrier pour mobile */
  .calendar-view {
    padding: 0.8rem;
  }
  
  .calendar-header {
    margin-bottom: 0.8rem;
  }
  
  .current-month {
    font-size: 1.3rem;
  }
  
  .calendar-grid {
    gap: 3px;
  }
  
  .day-header {
    padding: 0.3rem;
    font-size: 0.8rem;
  }
  
  .calendar-day {
    height: auto;
    width: auto;
    aspect-ratio: 1/1;
    padding: 0.3rem;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
  }
  
  .day-number {
    font-size: 0.85rem;
  }
  
  .has-availability .availability-indicator {
    width: 6px;
    height: 6px;
    bottom: 3px;
    right: 3px;
  }
  
  /* Améliorations pour la vue liste */
  .list-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.8rem;
  }
  
  .filter-controls {
    width: 100%;
  }
  
  .filter-select {
    width: 100%;
  }
  
  .availability-list-container {
    max-height: 400px;
  }
  
  .availability-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.6rem;
    padding: 0.8rem;
  }
  
  .availability-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  /* Ajustements pour les modals */
  .modal-container {
    width: 95%;
    max-height: 85vh;
  }
  
  .modal-header {
    padding: 1rem;
  }
  
  .modal-body {
    padding: 1rem;
  }
  
  .form-input {
    padding: 0.7rem 0.9rem;
  }
  
  .modal-footer {
    padding: 0.8rem 1rem;
    flex-direction: column;
    gap: 0.6rem;
  }
  
  .modal-footer .action-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .planning-title {
    font-size: 1.4rem;
  }
  
  .btn-text {
    display: none;
  }
  
  .action-btn.primary-btn {
    justify-content: center;
  }
  
  .action-btn, .toggle-btn {
    padding: 0.5rem;
  }
  
  .toggle-btn span:not(.toggle-icon) {
    display: none;
  }
  
  .calendar-grid {
    gap: 2px;
  }
  
  .day-header {
    font-size: 0.7rem;
    padding: 0.2rem;
  }
  
  .calendar-day {
    padding: 0.2rem;
  }
  
  .day-number {
    font-size: 0.75rem;
  }
  
  .availability-time {
    width: 100%;
  }
  
  .icon-btn {
    font-size: 1rem;
  }
  
  .day-details h4 {
    font-size: 1rem;
  }
  
  /* Amélioration pour l'état vide */
  .empty-state {
    padding: 2rem 1rem;
  }
  
  .empty-icon {
    font-size: 2.5rem;
  }
  
  .empty-state h4 {
    font-size: 1.1rem;
  }
  
  .empty-state p {
    font-size: 0.9rem;
  }
  
  /* Fix pour les détails de disponibilité */
  .availability-details p {
    font-size: 0.9rem;
  }
  
  /* Ajustement compact pour le header du calendrier */
  .calendar-header {
    padding: 0.2rem 0;
  }
  
  /* Optimisation des boutons d'action dans la liste des disponibilités */
  .availability-actions {
    gap: 0.3rem;
  }
}

/* Orientation landscape spécifique pour les mobiles */
@media (max-height: 600px) and (orientation: landscape) {
  .planning-container {
    padding: 5px;
  }
  
  .planning-card {
    padding: 0.8rem;
    margin: 5px 0;
  }
  
  .planning-title {
    font-size: 1.3rem;
    margin-bottom: 0.8rem;
  }
  
  .calendar-day {
    height: 30px;
  }
  
  .modal-container {
    max-height: 90vh;
  }
  
  /* Layout horizontal pour les modals en landscape */
  .modal-body {
    max-height: 50vh;
    overflow-y: auto;
  }
}

/* Styles pour les appareils à écran très petit */
@media (max-width: 320px) {
  .planning-title {
    font-size: 1.2rem;
  }
  
  .calendar-grid {
    gap: 1px;
  }
  
  .day-header, .day-number {
    font-size: 0.7rem;
  }
  
  .calendar-day {
    padding: 0.1rem;
  }
  
  .has-availability .availability-indicator {
    width: 4px;
    height: 4px;
  }
  
  .availability-time {
    font-size: 0.85rem;
  }
  
  .availability-duration {
    font-size: 0.75rem;
  }
}
</style>