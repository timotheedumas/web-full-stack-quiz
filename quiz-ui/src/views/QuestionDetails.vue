<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import quizApiService from '@/services/QuizApiService';

const route = useRoute();
const router = useRouter();

const question = ref(null);

async function loadQuestion() {
  const questionId = route.params.id;
  const response = await quizApiService.getQuestionById(questionId);
  if (response && response.data) {
    question.value = response.data;
  }
}

async function deleteQuestion() {
  const confirmed = confirm('Supprimer cette question ?');
  if (!confirmed) return;

  const questionId = route.params.id;
  await quizApiService.deleteQuestion(questionId);
  router.push('/admin/questions');
}

function editQuestion() {
  router.push(`/admin/question/${route.params.id}/edit`);
}

function goBack() {
  router.push('/admin/questions');
}

onMounted(loadQuestion);
</script>

<template>
  <div class="container mt-4" v-if="question">
    <!-- 🔙 Bouton retour -->
    <button class="btn btn-secondary mb-3" @click="goBack">
      ⬅️ Retour à la liste des questions
    </button>

    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>Question #{{ question.position }}</h2>
      <div>
        <button class="btn btn-outline-primary me-2" @click="editQuestion">Éditer</button>
        <button class="btn btn-outline-danger" @click="deleteQuestion">Supprimer</button>
      </div>
    </div>

    <h4>{{ question.title }}</h4>
    <p>{{ question.text }}</p>

    <img v-if="question.image" :src="question.image" class="img-fluid mb-3" />

    <ul class="list-group">
      <li
        v-for="answer in question.possibleAnswers"
        :key="answer.id"
        class="list-group-item d-flex justify-content-between"
      >
        {{ answer.text }}
        <span v-if="answer.isCorrect" class="badge bg-success">✔</span>
      </li>
    </ul>
  </div>
</template>
