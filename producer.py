# Kafka Consumer

import json
import time
import uuid
from datetime import UTC, datetime

from kafka import KafkaProducer

input_file = open("bus-geodata.json")
json_geodata = json.load(input_file)

coordinates = json_geodata["features"][0]["geometry"]["coordinates"]


def generate_uuid():
    return uuid.uuid4()


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    allow_auto_create_topics=True,
)


# construct message and sent it to kafka
data = {}
data["busline"] = "0001"


def generate_checkpoints(coordinates: list):
    i = 0

    while i < len(coordinates):
        data["key"] = data["busline"] + "_" + str(generate_uuid())
        data["timestamp"] = str(datetime.now(UTC))
        data["longitude"] = coordinates[i][0]
        data["latitude"] = coordinates[i][1]
        message = json.dumps(data)

        print(message)

        producer.send(topic="bus-coordinates", value=message.encode("utf-8"))
        if (
            i == len(coordinates) - 1
        ):  # start from starting coordinates if bus reaches the destination
            i = 0
        i += 1
        time.sleep(1)
    producer.flush()


generate_checkpoints(coordinates=coordinates)
