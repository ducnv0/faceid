<template>
  <div class="container">
    <!-- Upload new photo -->
    <section>
      <h1>Upload photo</h1>
      <div class="d-flex my-5">
        <!-- <label for="formFileLg" class="form-label">Large file input example</label> -->
        <input class="form-control form-control-lg" id="formFileLg" type="file" @change="onFileSelected">
        <button class="btn btn-primary" @click="onUpload">Upload</button>
      </div>
    </section>

    <!-- Show all photos -->
    <section>
      <h1>All photos</h1>
      <div v-if="photos && photos.length">
        <div class="row row-cols-1 row-cols-sm-1 row-cols-md-3 g-3">
          <div class="col" v-for="photo in photos" :key="photo.id">
            <div style="position: relative">
              <img :src="photo.presigned_get_url" alt="There's something wrong with this image"
                class="card-img-top img-fluid" style="object-fit: cover; height: 20rem;">
              <div class="btn btn-outline-danger" style="position: absolute; top: 4px; right: 4px" @click="deletePhoto(photo.id)">&times;</div>
            </div>
          </div>
        </div>
      </div>

      <div v-else>
        <p>No Photo to display</p>
      </div>
    </section>

  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  data () {
    return {
      deleteId: null,
      selectedFile: null
    }
  },
  props: ['personId'],
  created: function () {
    this.$store.commit('setPersonId', this.personId)
    this.$store.dispatch('getPhotos')
  },
  computed: {
    ...mapGetters({ photos: 'statePhotos' })
  },
  methods: {
    ...mapActions([
      'createPhoto',
      'getPhotos',
      'deletePhoto',
      'uploadPhoto'
    ]),
    onFileSelected (event) {
      console.log(event)
      this.selectedFile = event.target.files[0]
    },
    onUpload () {
      if (this.selectedFile) {
        this.uploadPhoto(this.selectedFile)
        this.selectedFile = null
      } else {
        // TODO: Show err
        console.log('No FILE')
      }
    }
  }
}
</script>
