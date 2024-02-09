import paho.mqtt.client as mqtt
import time
import json
from walk2 import Walk
import cv2  

broker_address = "localhost"
port = 1883
topics = ["pod-1", "pod-2", "pod-3", "pod-4"]

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client = mqtt.Client("MQTT_Producer")
client.on_connect = on_connect

client.connect(broker_address, port=port)

walk = Walk()  

cap = cv2.VideoCapture(r"C:/Users/c000851700/Desktop/MQTT_Deployment/short_vids/Scab1_cut.mp4")

try:
    while True:
        for topic in topics:
            ret, frame = cap.read()
            if not ret:
                break
            processed_img, avg_intensity = walk.process(frame)
            message = {"value": avg_intensity}  
            client.publish(topic, json.dumps(message))
            print(f"Published to {topic}: {message}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Script stopped by user")

cap.release()

client.disconnect()
