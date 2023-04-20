import { createStore } from 'vuex'

import people from './modules/people'

export default createStore({
  modules: {
    people
  }
})
