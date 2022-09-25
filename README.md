# cat2mqtt

A very minimalistic project to use keras models to detect objects in the RTSP video stream and report the detected objects to mqtt.

The project motivation and goals were described here nikolak.com/cat2mqtt/ - I'm using it with custom models to detect my cat on the windowsill, but you can
always download existing models and use it as well.

# Requirements

You can run this code directly on your machine, other than `requirements.txt` requirements you also need tensorflow installed - the
version of which may depend on your architecture. I'd recommend running it in as a docker container. 
Note: Running this code as a docker container does not work on M1 CPUs at the time of writing.

You can take `docker-compose.sample.yaml` as your starting base.

# Environment variables


| Environment Variable | Description                                                                               | Example                   | Default        |
|----------------------|-------------------------------------------------------------------------------------------|---------------------------|----------------|
| MODEL_PATH           | The path to the keras model                                                               | /path/to/keras_model.h5   | keras_model.h5 |
| LABELS_PATH          | The path to labels for the above mentioned keras model                                    | /path/to/labels.txt       | labels.txt     |
| POSITIVE_LABEL       | Optional, will report to mqtt only if this label has the highest score                    | Testing                   | None           |
| CONFIDENCE_THRESHOLD | Optional, only report if the highest object score is higher than this. Between 0 and 1    | 0.25                      | 0              |
| RTSP_URL             | The URL to the RTSP stream to fetch the images from                                       | rtsp://1.2.3.4:7447/token | None           |
| MQTT_HOST            | MQTT Host                                                                                 | mqtt.example.com          | None           |
| MQTT_PORT            | MQTT Port                                                                                 | 1234                      | 1883           |
| MQTT_TOPIC           | Topic to report to. The confidence and label will be nested and reported under that topic | keras/bedroom             | None           |
| MQTT_USERNAME        | MQTT username to use                                                                      | username                  | None           |
| MQTT_PASSWORD        | Password for the above username to use                                                    | pwd                       | None           |
| SLEEP_TIME           | Optional time to sleep between detection attempts                                         | 10                        | 5              |

# License

MIT - see LICENSE for details