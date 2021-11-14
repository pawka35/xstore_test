import {Genres} from "./genres.js";
import {Actors} from "./actors.js";
import {Directors} from "./directors.js";

const routes = [
  { path: '/', component: Genres },
  { path: '/actors/', component: Actors },
  { path: '/directors/', component: Directors },
];

const router = new VueRouter({
    mode: 'history',
    routes: routes
});

new Vue({
  el: '#app',
  router: router,
})