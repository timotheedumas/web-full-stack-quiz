import axios from 'axios';

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true,
});

export default {
  async call(method, resource, data = null, token = null) {
    const headers = {
      'Content-Type': 'application/json',
    };

    // 🔐 Récupère automatiquement le token depuis localStorage
    if (!token) {
      token = localStorage.getItem('adminToken');
    }

    if (token) {
      headers.Authorization = 'Bearer ' + token;
    }

    const config = {
      method,
      url: resource,
      headers,
    };

    // ⚠️ Axios ne supporte pas data avec DELETE s’il est null
    if (method !== 'delete') {
      config.data = data;
    }

    return instance(config)
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
      });
  },

  getQuizInfo() {
    return this.call('get', 'quiz-info');
  },

  getQuestion(position) {
    return this.call('get', `questions?position=${position}`);
  },

  // 🆕 Envoie les réponses du joueur à l’API
  submitParticipation(playerName, answers) {
    return this.call('post', 'participations', {
      playerName,
      answers,
    });
  },

  getAllQuestions() {
    return this.call('get', 'questions');
  },

  getQuestionById(id) {
    return this.call('get', `questions/${id}`);
  },

  deleteQuestion(id) {
    return this.call('delete', `questions/${id}`);
  },
  updateQuestion(id, updatedData) {
    return this.call('put', `questions/${id}`, updatedData);
  },
  async createEmptyQuestion() {
    const quizInfo = await this.getQuizInfo();
    const nextPosition = (quizInfo.data?.size || 0) + 1;

    return this.call('post', 'questions', {
      title: 'Nouvelle question',
      text: '',
      image: '',
      position: nextPosition,
      possibleAnswers: [
        { text: '', isCorrect: false },
        { text: '', isCorrect: false },
        { text: '', isCorrect: false },
        { text: '', isCorrect: false },
      ],
    });
  },
};
