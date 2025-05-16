<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService';

const username = ref('');
const router = useRouter();

console.log('NewQuizPage mounted');

function launchNewQuiz() {
  participationStorageService.savePlayerName(username.value);
  console.log('Nom sauvegardé :', username.value);
  router.push('/question/1'); // ✅ redirection vers la première question
}
</script>

<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">Démarrage du quiz</h1>

    <p>Saisissez votre nom :</p>

    <input type="text" class="form-control mb-3" placeholder="Username" v-model="username" />

    <p>{{ username }}</p>

    <button class="btn btn-outline-danger w-100" @click="launchNewQuiz">GO!</button>
  </div>
</template>
