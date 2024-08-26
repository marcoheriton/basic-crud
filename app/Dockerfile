FROM python:3.10-bullseye

LABEL criador="Marcoheriton"
WORKDIR /app
COPY . /app/
RUN pip install --upgrade pip && pip install -r requeriments.txt
EXPOSE 8501
ENTRYPOINT [ "streamlit", "run", "app.py" ]