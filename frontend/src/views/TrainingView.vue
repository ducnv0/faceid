<template>
  <div class="container">
    <button @click="onTraining" :disabled="isTraining" class="btn btn-primary" type="button">
      <span class="sr-only">{{ buttonText }}</span>
      <span v-if="isTraining" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    </button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      isTraining: false
    }
  },
  computed: {
    buttonText () {
      return this.isTraining ? 'Training...' : 'Train'
    }
  },
  methods: {
    async onTraining () {
      this.isTraining = true
      await axios.post('/api/v1/faceid/train')
      this.isTraining = false
    }
  }
}
</script>
