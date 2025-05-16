import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import NewQuizPage from '../views/NewQuizPage.vue';
import QuestionPage from '../views/QuestionPage.vue';
import QuestionsAdmin from '../views/QuestionsAdmin.vue';
import ScorePage from '../views/ScorePage.vue';
import AdminLogin from '../views/AdminLogin.vue';
import QuestionDetails from '../views/QuestionDetails.vue';
import QuestionEdit from '../views/QuestionEdit.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage,
    },
    {
      path: '/new-quiz',
      name: 'NewQuizPage',
      component: NewQuizPage,
    },
    {
      path: '/admin/questions',
      name: 'QuestionsAdmin',
      component: QuestionsAdmin,
    },
    {
      path: '/question/:position',
      name: 'QuestionPage',
      component: QuestionPage,
    },
    {
      path: '/score',
      name: 'ScorePage',
      component: ScorePage,
    },
    {
      path: '/admin/login',
      name: 'AdminLogin',
      component: AdminLogin,
    },
    {
      path: '/admin/question/:id',
      name: 'QuestionDetails',
      component: QuestionDetails,
    },
    {
      path: '/admin/question/:id/edit',
      name: 'QuestionEdit',
      component: QuestionEdit,
    },
  ],
});

// 🔐 Guard pour protéger les routes admin
router.beforeEach((to, from, next) => {
  const isAdmin = localStorage.getItem('isAdmin') === 'true';

  if (to.path.startsWith('/admin') && to.path !== '/admin/login' && !isAdmin) {
    // Si l'utilisateur tente d'accéder à une page admin sans être connecté
    next('/admin/login');
  } else {
    next(); // Autorisé
  }
});

export default router;
