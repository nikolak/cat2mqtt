from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2
import os
import time
import paho.mqtt.client as mqtt

if not os.environ.get("OPENCV_FFMPEG_CAPTURE_OPTIONS"):
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"


class Cat2mqtt:

    def __init__(self):
        # Model data
        self.model = load_model(os.environ.get('MODEL_PATH', 'keras_model.h5'))
        with open(os.environ.get('LABELS_PATH', 'labels.txt'), "r") as labels_file:
            self.labels = {int(_[0]): _[1] for _ in [_.split() for _ in labels_file.readlines()]}
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Detection configuration
        self.positive_label = os.environ.get('POSITIVE_LABEL', None)
        self.confidence_threshold = os.environ.get('CONFIDENCE_THRESHOLD', 0)

        # mqtt setup
        self.mqtt_topic = os.environ.get('MQTT_TOPIC')
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.username_pw_set(username=os.environ.get('MQTT_USERNAME'),
                                         password=os.environ.get('MQTT_PASSWORD'))
        self.mqtt_client.connect(os.environ.get('MQTT_HOST'), os.environ.get('MQTT_PORT', 1883))
        self.mqtt_client.loop_start()

    def get_image_array(self):
        vcap = cv2.VideoCapture(os.environ.get('RTSP_URL'), cv2.CAP_FFMPEG)
        ret, frame = vcap.read()
        if ret is False:
            print("empty frame")
            return None

        image = Image.fromarray(frame)
        image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        return normalized_image_array

    def image_to_array(self, image):
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        return normalized_image_array

    def detect(self, normalized_image_array):
        self.data[0] = normalized_image_array
        prediction = self.model.predict(self.data)
        return float(prediction.max()), self.labels[prediction.argmax()]

    def send_to_mqtt(self, confidence, label):
        if confidence > self.confidence_threshold:
            if self.positive_label and self.positive_label != label:
                return
            self.mqtt_client.publish(self.mqtt_topic + '/label', label)
            self.mqtt_client.publish(self.mqtt_topic + '/confidence', confidence)

    def loop(self):
        _sleep_time = int(os.environ.get('SLEEP_TIME', 5))
        while True:
            image_array = self.get_image_array()
            if image_array is not None:
                confidence, label = self.detect(image_array)
                self.send_to_mqtt(confidence, label)
            time.sleep(_sleep_time)


if __name__ == '__main__':
    cat2mqtt = Cat2mqtt()
    cat2mqtt.loop()
