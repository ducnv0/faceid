// FIXME: this file is run at build stage, it does not know about environment variable that are added by docker-compose
export const settings = {
  API_DOMAIN: process.env.API_DOMAIN || 'http://localhost:8080'
}
