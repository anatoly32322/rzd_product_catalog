FROM python:3.9-slim

ARG iam_token
ARG folder_id

ENV IAM_TOKEN=$iam_token
ENV FOLDER_ID=$folder_id

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py"]