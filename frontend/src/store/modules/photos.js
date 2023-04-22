import axios from 'axios'

const state = {
  personId: null,
  photos: null
}

const getters = {
  statePersonId: state => state.personId,
  statePhotos: state => state.photos
}

const mutations = {
  setPhotos (state, photos) {
    state.photos = photos
  },
  setPersonId (state, personId) {
    state.personId = personId
  }
}

const actions = {
  async createPhoto ({ dispatch, state }, photo) {
    await axios.post(`/api/v1/faceid/photos/person/${state.personId}`, photo)
    await dispatch('getPhotos')
  },
  async getPhotos ({ commit, state }) {
    const { data } = await axios.get(`/api/v1/faceid/photos/person/${state.personId}`)
    commit('setPhotos', data)
  },
  async deletePhoto ({ dispatch }, id) {
    await axios.delete(`/api/v1/faceid/photos/${id}`)
    await dispatch('getPhotos')
  },
  async uploadPhoto ({ state, dispatch }, file) {
    const { data } = await axios.get(`/api/v1/faceid/photos/presigned_put/person/${state.personId}/`)
    console.log(typeof data)
    console.log(data)
    const presignedPutUrl = data.presigned_put_url
    await axios.put(presignedPutUrl, file)
    console.log('DONE UPLOAD')
    await axios.post(`/api/v1/faceid/photos/person/${state.personId}`, data)
    await dispatch('getPhotos')
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
