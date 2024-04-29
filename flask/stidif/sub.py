# python 3.11

import random

from paho.mqtt import client as mqtt_client


broker = 'broker.envisionsapp.com'
port = 1883
topic = "/STIDIF/STIDIF-PROTOTYPE"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'digimqtt'
password = 'pahlawan10'

# Variabel global untuk menyimpan data MQTT yang diterima
mqtt_data = {}


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    # Misalkan pesan yang diterima memiliki format "ON" atau "OFF" untuk mengontrol saklar
    if msg.payload.decode() == "ON":
        # Logika untuk menyalakan saklar
        print("Turning the switch ON")
        # Tambahkan kode untuk menyalakan saklar sesuai dengan format yang diperlukan
    elif msg.payload.decode() == "OFF":
        # Logika untuk mematikan saklar
        print("Turning the switch OFF")
        # Tambahkan kode untuk mematikan saklar sesuai dengan format yang diperlukan
    else:
        print("Invalid command")

def subscribe(client: mqtt_client):
    client.subscribe(topic)
    client.on_message = on_message

    # Fungsi callback on_message yang akan mengupdate variabel global mqtt_data
    def on_message_update_mqtt_data(client, userdata, msg):
        global mqtt_data
        mqtt_data[msg.topic] = msg.payload.decode()

    # Set callback on_message_update_mqtt_data sebagai callback untuk menerima pesan
    client.message_callback_add(topic, on_message_update_mqtt_data)


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()



if __name__ == '__main__':
    run()
