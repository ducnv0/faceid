import axios from 'axios'

const state = {
  people: null,
  person: null
}

const getters = {
  statePeople: state => state.people,
  statePerson: state => state.person
}

const mutations = {
  setPerson (state, person) {
    state.person = person
  },
  setPeople (state, people) {
    state.people = people
  }
}

const actions = {
  async createPerson ({ dispatch }, person) {
    console.log(`test ${person}`)
    await axios.post('/api/v1/faceid/people', person)
    await dispatch('getPeople')
  },
  async getPeople ({ commit }) {
    const { data } = await axios.get('/api/v1/faceid/people')
    commit('setPeople', data)
  },
  async updatePerson ({ dispatch }, person) {
    await axios.patch(`people/${person.id}`, person.form)
    await dispatch('getPeople')
  },
  async deletePerson ({ dispatch }, id) {
    await axios.delete(`/api/v1/faceid/people/${id}`)
    await dispatch('getPeople')
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
