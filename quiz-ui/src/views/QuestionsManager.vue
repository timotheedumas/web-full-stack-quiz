<script setup>
import { ref, onMounted } from 'vue';
import QuestionDisplay from '@/components/QuestionDisplay.vue';
import quizApiService from '@/services/QuizApiService';

const currentQuestion = ref(null);
const currentPosition = ref(1);
const totalQuestions = ref(0);

async function loadQuestionByPosition(position) {
  const response = await quizApiService.getQuestion(position);
  console.log('Question chargée :', response);
  if (response && response.data) {
    currentQuestion.value = response.data; // ✅ correspond à ton API
  } else {
    console.warn('Pas de question trouvée à la position', position);
  }
}

function answerClickedHandler(answerId) {
  console.log('Réponse sélectionnée :', answerId);
  if (currentPosition.value < totalQuestions.value) {
    currentPosition.value += 1;
    loadQuestionByPosition(currentPosition.value);
  } else {
    endQuiz();
  }
}

function endQuiz() {
  console.log('Fin du quiz !');
  // TODO : redirection vers la page des scores plus tard
}

onMounted(async () => {
  const response = await quizApiService.getQuizInfo();
  console.log('Réponse quiz-info :', response);
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
