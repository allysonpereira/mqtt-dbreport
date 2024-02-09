import paho.mqtt.client as mqtt
import json
import mysql.connector
from datetime import datetime
from collections import deque
from datetime import datetime
import time

# the idea of this script is to update the previous consume.py script by adding deque and dictionary to it.
# it is being done by creating a dictionary, where the key is the topic and the value will be a deque.
# this is one script that works with another scrip where one subscribe to the topics, writting to the...
# database, while the ohter is listening and tried to figure out if on a specific pode, there is a scab.

with open('myjson.json', 'r') as json_file:
    config = json.load(json_file)

broker_address = config['messenger']['broker_address']
port = config['messenger']['port']

mysql_config = config['mysql']

deques_dict = {}
scab_dict = {}

def on_connect(client, userdata, flags, rc):
    client.subscribe("#")

def on_message(client, userdata, msg):
    message = json.loads(msg.payload)
    value = float(message["value"])
    topic = msg.topic

    # checks if a deque for the received topic exists in the deques_dict
    # if not, it initializes a new deque with a maximum length of 5 and associates it with the topic
    if topic not in deques_dict: 
        deques_dict[topic] = deque(maxlen=5)

    if topic not in scab_dict:
        scab_dict[topic] = False


    deques_dict[topic].append(value)

    print(f"Received '{value}' from '{topic}' topic")

    try:
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        query = "INSERT INTO Tuyere_Data (pod_id, timestamp, value) VALUES (%s, %s, %s)"
        data = (topic, str(datetime.now()), value)
        cursor.execute(query, data)

        connection.commit()
        cursor.close()
        connection.close()
        print("Data inserted into MySQL database.")

    except Exception as e:
        print(f"Error: {e}")

    for key, d in deques_dict.items():
        print(f"{key}: {list(d)}")

client = mqtt.Client("MQTT_Consumer2")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=port)
client.loop_forever()