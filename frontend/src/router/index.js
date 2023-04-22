import { createRouter, createWebHistory } from 'vue-router'
import PeopleView from '../views/PeopleView.vue'
import PhotosView from '../views/PhotosView.vue'
import DetectionView from '../views/DetectionView.vue'

const routes = [
  {
    path: '/people',
    name: 'people',
    component: PeopleView
  },
  {
    path: '/photos/person/:personId',
    name: 'photos',
    component: PhotosView,
    props: true
  },
  {
    path: '/detection',
    name: 'detection',
    component: DetectionView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
