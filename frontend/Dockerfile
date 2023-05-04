# FIXME: https://cli.vuejs.org/guide/deployment.html#docker-nginx
# This dockerfile just A TEMPORARY DEMO
FROM node:12.22.9-slim

WORKDIR /opt
COPY package*.json ./
RUN npm install

COPY ./ .

EXPOSE 8081

RUN chmod +x ./scripts/run_app.sh
CMD ["./scripts/run_app.sh"]
