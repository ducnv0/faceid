<template>
  <div class="container">
    <!-- Register new person -->
    <section class="mb-5">
      <h1>Register new person</h1>
      <div class="mb-3">
        <label for="fullName" class="form-label">Full Name</label>
        <input type="text" class="form-control" id="fullName" v-model="form.full_name">
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Email address</label>
        <input type="email" class="form-control" id="email" aria-describedby="emailHelp" v-model="form.email">
      </div>
      <button class="btn btn-primary" @click="register">Register</button>
    </section>

    <!-- Show all people -->
    <section v-if="people && people.length">
      <h1>All people</h1>
      <div class="row row-cols-1 row-cols-sm-1 row-cols-md-3 g-3">

        <div class="col" v-for="person in people" :key="person.id">
          <div class="card">
            <img src="https://source.unsplash.com/featured" alt="..." class="card-img-top img-fluid"
              style="object-fit: cover; height: 20rem;">
            <div class="card-body">
              <h5 class="card-title">{{ person.full_name }}</h5>
              <h6 class="card-subtitle text-muted ">{{ person.email }}</h6>
              <div class="btn-group mt-2" role="group" aria-label="Basic example">
                <button type="button" class="btn btn-outline-primary">Edit</button>
                <router-link :to="{name: 'photos', params: {personId: person.id}}" class="btn btn-outline-primary">
                  <span>Photos</span>
                </router-link>
                <!-- <button type="button" class="btn btn-outline-primary">Photos</button> -->
                <button type="button" class="btn btn-outline-secondary">Disable</button>
                <button type="button" class="btn btn-outline-danger" @click="deletePerson(person.id)">Delete</button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>

    <div v-else>
      <p>No person</p>
    </div>

  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  data () {
    return {
      form: {
        full_name: '',
        email: ''
      },
      deleteId: null
    }
  },
  created: function () {
    return this.$store.dispatch('getPeople')
  },
  computed: {
    ...mapGetters({ people: 'statePeople' })
  },
  methods: {
    ...mapActions([
      'createPerson',
      'deletePerson'
    ]),
    async register () {
      await this.createPerson(this.form)
    }
  }
}
</script>
