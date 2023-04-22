import { createStore } from 'vuex'

import people from './modules/people'
import photos from './modules/photos'

export default createStore({
  modules: {
    people,
    photos
  }
})
