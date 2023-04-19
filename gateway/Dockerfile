FROM python:3.9.16

# install deepface lib
RUN apt-get update
RUN apt-get install ffmpeg -y
RUN pip install deepface==0.0.79
COPY ./scripts/download_models.sh ./scripts/download_models.sh
RUN chmod +x ./scripts/download_models.sh && ./scripts/download_models.sh

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /opt
COPY ./external_utils ./external_utils
COPY ./scripts ./scripts
COPY ./src ./src

EXPOSE 8080

RUN chmod +x ./scripts/run_app.sh
CMD ["./scripts/run_app.sh"]
