<template>
  <nav class="navbar navbar-expand-sm bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">FaceID</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link :to="{ name: 'people' }" class="nav-link">
              <span>People</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="#" class="nav-link">
              <span>Face Detection</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="#" class="nav-link">
              <span>Face Recognition</span>
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <router-view/>
</template>
