FROM tensorflow/tensorflow:2.10.0

WORKDIR /app

COPY requirements.txt requirements.txt
COPY main.py main.py
RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD ["python", "main.py"]