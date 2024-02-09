import paho.mqtt.client as mqtt
import json
import mysql.connector
from datetime import datetime

with open('myjson.json', 'r') as json_file: 
    config = json.load(json_file) # saves the data from myjson and stores into config

broker_address = config['messenger']['broker_address'] # retrieves the mqtt broker address and port
port = config['messenger']['port'] 

mysql_config = config['mysql'] # retrieves the mysql configuration from config

def on_connect(client, userdata, flags, rc): # subscribe to all topics # when the mqtt client is connected
    client.subscribe("#")

def on_message(client, userdata, msg): # process incoming mqtt mesages
    message = json.loads(msg.payload) # retrieve the json payload of the message
    value = int(message["value"]) # extract value
    topic = msg.topic # extract topic
    print(f"Received '{value}' from '{topic}' topic") # print value and topic to the console

    try:
        connection = mysql.connector.connect(**mysql_config) # connects to the database
        cursor = connection.cursor()

        # defines a query to add data into the table
        query = "INSERT INTO Tuyere_Data (pod_id, timestamp, value) VALUES (%s, %s, %s)"
        data = (topic, str(datetime.now()), value) 
        cursor.execute(query, data)

        connection.commit()
        cursor.close()
        connection.close()
        print("Data inserted into MySQL database.")

    except Exception as e:
        print(f"Error: {e}")

client = mqtt.Client("MQTT_Consumer") # creates a mqtt client mqtt_consumer
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=port) 
client.loop_forever() # starts the mqtt main loop that keeps listening for incoming messages
