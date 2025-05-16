<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService';
import quizApiService from '@/services/QuizApiService';
import Leaderboard from '@/components/Leaderboard.vue'; // ✅ ajout de l'import

const router = useRouter();

const playerName = ref('');
const score = ref(null);
const leaderboard = ref([]);

onMounted(async () => {
  playerName.value = participationStorageService.getPlayerName();
  score.value = participationStorageService.getParticipationScore();

  const response = await quizApiService.getQuizInfo();
  if (response && response.data && Array.isArray(response.data.scores)) {
    leaderboard.value = response.data.scores;
  }
});

function returnToHome() {
  participationStorageService.clear();
  router.push('/');
}
</script>

<template>
  <div class="container mt-4 text-center">
    <h1 class="mb-4">🎉 Fin du quiz !</h1>

    <div class="mb-4">
      <h2>{{ playerName }}, ton score est :</h2>
      <div class="display-4">{{ score }}</div>
    </div>

    <div class="mb-4">
      <h3>Classement</h3>
      <Leaderboard :scores="leaderboard" :highlight="playerName" />
      <!-- ✅ remplacement -->
    </div>

    <button class="btn btn-outline-primary mt-3" @click="returnToHome">Retour à l'accueil</button>
  </div>
</template>
