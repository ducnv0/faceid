<template>
  <div class="container">
    <button class="btn btn-primary my-3">Register New Person</button>

    <div class="row row-cols-1 row-cols-sm-1 row-cols-md-3 g-3">

      <div class="col" v-for="(person, i) in peoples" :key="i">
        <div class="card">
          <img src="https://source.unsplash.com/featured" alt="..." class="card-img-top img-fluid"
            style="object-fit: cover; height: 20rem;">
          <div class="card-body">
            <h5 class="card-title">Nguyen Van Duc</h5>
            <h6 class="card-subtitle text-muted ">nguyenvanducwork@gmail.com</h6>
            <div class="btn-group mt-2" role="group" aria-label="Basic example">
              <button type="button" class="btn btn-outline-primary">Edit</button>
              <button type="button" class="btn btn-outline-primary">Photos</button>
              <button type="button" class="btn btn-outline-secondary">Disable</button>
              <button type="button" class="btn btn-outline-danger">Delete</button>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      peoples: [
        {
          id: 0, full_name: 'Nguyen Van Duc', email: 'nguyenvanducwork@gmail.com'
        },
        {
          id: 0, full_name: 'Nguyen Van Duc', email: 'nguyenvanducwork@gmail.com'
        },
        {
          id: 0, full_name: 'Nguyen Van Duc', email: 'nguyenvanducwork@gmail.com'
        },
        {
          id: 0, full_name: 'Nguyen Van Duc', email: 'nguyenvanducwork@gmail.com'
        },
        {
          id: 0, full_name: 'Nguyen Van Duc', email: 'nguyenvanducwork@gmail.com'
        },
        {
          id: 0, full_name: 'Nguyen Van Duc', email: 'nguyenvanducwork@gmail.com'
        },
        {
          id: 0, full_name: 'Nguyen Van Duc', email: 'nguyenvanducwork@gmail.com'
        }
      ]
    }
  }
}
</script>
