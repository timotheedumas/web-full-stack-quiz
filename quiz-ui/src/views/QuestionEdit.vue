<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import quizApiService from '@/services/QuizApiService';

const route = useRoute();
const router = useRouter();
const id = route.params.id;

const question = ref({
  position: 1,
  title: '',
  text: '',
  image: '',
  possibleAnswers: [
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
  ],
});

async function load() {
  const response = await quizApiService.getQuestionById(id);
  if (response && response.data) {
    question.value = response.data;
  }
}

function setCorrect(index) {
  question.value.possibleAnswers.forEach((a, i) => {
    a.isCorrect = i === index;
  });
}

function handleImageUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = () => {
    question.value.image = reader.result;
  };
  reader.readAsDataURL(file);
}

async function save() {
  console.log('Données envoyées :', question.value); // 🔍 Vérifie ce qui part

  const response = await quizApiService.updateQuestion(id, question.value);

  console.log('Réponse back :', response); // 🔍 Vérifie le retour HTTP

  if (response.status === 204) {
    router.push('/admin/questions');
  }
}

function cancel() {
  router.push('/admin/questions');
}

onMounted(load);
</script>

<template>
  <div class="container mt-4">
    <h2>Modifier une question</h2>

    <div class="mb-3">
      <label>Position</label>
      <input v-model="question.position" type="number" class="form-control" />
    </div>

    <div class="mb-3">
      <label>Titre</label>
      <input v-model="question.title" type="text" class="form-control" />
    </div>

    <div class="mb-3">
      <label>Intitulé</label>
      <textarea v-model="question.text" class="form-control" />
    </div>

    <div class="mb-3">
      <label>Image</label>
      <input type="file" accept="image/*" @change="handleImageUpload" class="form-control" />
      <div v-if="question.image" class="mt-3">
        <p class="mb-1">Aperçu de l’image :</p>
        <img :src="question.image" class="img-fluid" style="max-height: 200px" />
      </div>
    </div>

    <h5>Réponses possibles :</h5>
    <div v-for="(answer, index) in question.possibleAnswers" :key="index" class="mb-2">
      <input v-model="answer.text" type="text" class="form-control mb-1" />
      <div class="form-check">
        <input
          class="form-check-input"
          type="radio"
          :checked="answer.isCorrect"
          @change="setCorrect(index)"
        />
        <label class="form-check-label">Réponse correcte</label>
      </div>
    </div>

    <button class="btn btn-primary me-2" @click="save">💾 Sauvegarder</button>
    <button class="btn btn-secondary" @click="cancel">Annuler</button>
  </div>
</template>
