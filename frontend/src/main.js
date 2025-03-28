import { createApp } from 'vue';
import App from './App.vue'; // Make sure App.vue exists
import router from './routes';

const app = createApp(App);
app.use(router);
app.mount('#app');
