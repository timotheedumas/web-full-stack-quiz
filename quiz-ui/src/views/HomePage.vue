<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';
import Leaderboard from '@/components/Leaderboard.vue'; // ✅ ajout de l'import

const registeredScores = ref([]);

onMounted(async () => {
  console.log('Home page mounted');
  const response = await quizApiService.getQuizInfo();
  if (response && response.data && response.data.scores) {
    registeredScores.value = response.data.scores;
    console.log('Scores chargés :', registeredScores.value);
  }
});
</script>

<template>
  <div class="container mt-4">
    <h1 class="text-center mb-4">Home page</h1>

    <div v-if="registeredScores.length === 0" class="alert alert-warning">
      Aucun score enregistré pour le moment.
    </div>

    <div v-else>
      <h2 class="h4">Meilleurs scores :</h2>
      <Leaderboard :scores="registeredScores" />
      <!-- ✅ remplacement -->
    </div>

    <router-link to="/new-quiz" class="btn btn-primary mt-4 w-100">
      Démarrer le quiz !
    </router-link>
  </div>
</template>
