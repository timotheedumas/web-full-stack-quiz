<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import quizApiService from '@/services/QuizApiService';

const questions = ref([]);
const router = useRouter();

function logout() {
  localStorage.removeItem('isAdmin');
  router.push('/');
}

function goToQuestion(id) {
  router.push(`/admin/question/${id}`);
}

async function createQuestion() {
  const response = await quizApiService.createEmptyQuestion();
  if (response && response.data && response.data.id) {
    router.push(`/admin/question/${response.data.id}/edit`);
  } else {
    console.warn('Erreur lors de la création de la question');
  }
}

onMounted(async () => {
  const response = await quizApiService.getQuizInfo();
  if (response && response.data && Array.isArray(response.data.questions)) {
    questions.value = response.data.questions;
  } else {
    console.warn('Aucune question trouvée dans quiz-info');
  }
});
</script>

<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Administration des questions</h1>
      <button class="btn btn-outline-danger" @click="logout">Déconnexion</button>
    </div>

    <button class="btn btn-success mb-3" @click="createQuestion">➕ Créer une question</button>

    <ul class="list-group">
      <li
        v-for="question in questions"
        :key="question.id"
        class="list-group-item list-group-item-action"
        @click="goToQuestion(question.id)"
        style="cursor: pointer"
      >
        <strong>#{{ question.position }} -</strong> {{ question.title }}
      </li>
    </ul>
  </div>
</template>
