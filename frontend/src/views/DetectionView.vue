<!-- Get the idea from https://codepen.io/ditarahma08/pen/GRRxZLW -->
<template>
  <div class="container">

    <!-- <form id="form-connect">
      <div class="input-group mb-3">
        <select id="camera-select"></select>
        <button class="btn btn-success" type="submit" id="button-start">Start</button>
      </div>
    </form>
    <div class="position-relative">
      <video ref="videoEl" autoplay="true" playsinline></video>
      <canvas ref="canvasEl" class="position-absolute top-0 start-0"></canvas>
    </div> -->

    <div class="web-camera-container">
      <div class="camera-button">
        <button type="button" class="btn"
          :class="{ 'btn-success': !isCameraOpen, 'btn-danger': isCameraOpen }" @click="toggleCamera">
          <span v-if="!isCameraOpen">Start</span>
          <span v-else>Stop</span>
        </button>
      </div>

      <div v-show="isCameraOpen" class="position-relative">
        <video ref="video" class="w-75" autoplay></video>
        <canvas ref="canvas" class="position-absolute top-0 start-0 w-75"></canvas>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  data () {
    return {
      isCameraOpen: false,
      connection: null,
      image_interval_ms: 100,
      intervalId: null
    }
  },
  methods: {
    toggleCamera () {
      if (this.isCameraOpen) {
        this.stopDetection()
      } else {
        this.startDetection()
      }
    },
    createCameraElement () {
      const constraints = {
        audio: false,
        video: true
      }
      navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
        this.$refs.video.srcObject = stream
      }).catch((err) => {
        alert(`Got error when loading camera ${err}`)
      })
    },
    stopCameraStream () {
      const tracks = this.$refs.video.srcObject.getTracks()
      tracks.forEach(track => {
        track.stop()
      })
    },
    establishConnection () {
      console.log('Establish new websocket connection')
      this.connection = new WebSocket('ws://localhost:8080/api/v1/faceid/detect')
      this.connection.onopen = (event) => {
        console.log(event)
        console.log('Successfully connected to websocket server')
      }
      this.connection.onmessage = (event) => {
        this.drawFaceBoxes(JSON.parse(event.data))
      }
      this.connection.onclose = (event) => {
        console.log(event)
        console.log('Successfully closed connection')
      }
    },
    closeConnection () {
      this.connection.close()
    },
    startDetection () {
      this.createCameraElement()
      this.isCameraOpen = true
      this.establishConnection()
      // capture and send images to server
      this.intervalId = setInterval(() => {
        const ctx = this.$refs.canvas.getContext('2d')
        this.$refs.canvas.width = this.$refs.video.videoWidth
        this.$refs.canvas.height = this.$refs.video.videoHeight
        ctx.drawImage(this.$refs.video, 0, 0)
        this.$refs.canvas.toBlob((blob) => {
          if (blob) {
            console.log(blob)
            this.connection.send(blob)
          } else {
            // TODO: Find out why we get a null here???
            console.log('Got blob null')
          }
        }, 'image/jpeg')
      }, this.image_interval_ms)
    },
    stopDetection () {
      clearInterval(this.intervalId)
      this.stopCameraStream()
      this.closeConnection()
      this.isCameraOpen = false
    },
    drawFaceBoxes (faces) {
      const ctx = this.$refs.canvas.getContext('2d')
      ctx.width = this.$refs.video.videoWidth
      ctx.height = this.$refs.video.videoHeight
      ctx.strokeStyle = '#49fb35'
      ctx.beginPath()
      ctx.clearRect(0, 0, ctx.width, ctx.height)
      for (const face of faces) {
        ctx.beginPath()
        ctx.rect(face.x, face.y, face.w, face.h)
        ctx.stroke()
      }
    }
  }
}
</script>
