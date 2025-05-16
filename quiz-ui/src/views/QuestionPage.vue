<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import QuestionDisplay from '@/components/QuestionDisplay.vue';
import quizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';

const route = useRoute();
const router = useRouter();

const currentPosition = ref(parseInt(route.params.position || '1'));
const totalQuestions = ref(0);
const currentQuestion = ref(null);
const selectedAnswers = ref([]); // 🆕 Stocke les réponses sélectionnées

async function loadQuestionByPosition(position) {
  const response = await quizApiService.getQuestion(position);
  console.log('Question chargée :', response);
  if (response && response.data) {
    currentQuestion.value = response.data;
  } else {
    console.warn('Pas de question trouvée à la position', position);
  }
}

function answerClickedHandler(answerId) {
  if (selectedAnswers.value.length >= totalQuestions.value) return;

  // 🔁 Trouver l'indice de 0 à 3, puis ajouter 1
  const index = currentQuestion.value.possibleAnswers.findIndex((a) => a.id === answerId);

  if (index === -1) {
    console.warn('Réponse non trouvée dans possibleAnswers');
    return;
  }

  selectedAnswers.value.push(index + 1); // ✅ 1-based index attendu par l'API
  console.log('Réponse sélectionnée (index + 1) :', index + 1);

  if (currentPosition.value < totalQuestions.value) {
    const nextPosition = currentPosition.value + 1;
    router.push(`/question/${nextPosition}`);
  } else {
    endQuiz();
  }
}

async function endQuiz() {
  const playerName = participationStorageService.getPlayerName();
  const answers = [...selectedAnswers.value]; // 🟢 déstructure le ref pour avoir un vrai tableau

  console.log('Envoi participation', { playerName, answers });

  try {
    const response = await quizApiService.submitParticipation(playerName, answers);
    if (response && response.data && typeof response.data.score === 'number') {
      const score = response.data.score;
      participationStorageService.saveParticipationScore(score);
      router.push('/score');
    } else {
      console.warn('Erreur : réponse de participation invalide');
    }
  } catch (error) {
    console.error('Erreur lors de l’envoi de la participation', error);
  }
}

// 🔁 Recharge quand l’URL change (position)
watch(
  () => route.params.position,
  async (newVal) => {
    currentPosition.value = parseInt(newVal || '1');
    await loadQuestionByPosition(currentPosition.value);
  }
);

onMounted(async () => {
  const response = await quizApiService.getQuizInfo();
  if (response && response.data) {
    totalQuestions.value = response.data.size;
    await loadQuestionByPosition(currentPosition.value);
  } else {
    console.warn('Impossible de récupérer quiz-info');
  }
});
</script>

<template>
  <div class="container mt-4" v-if="currentQuestion">
    <h1 class="mb-4">Question {{ currentPosition }} / {{ totalQuestions }}</h1>
    <QuestionDisplay :question="currentQuestion" @click-on-answer="answerClickedHandler" />
  </div>
</template>
