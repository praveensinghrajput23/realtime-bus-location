import json
import threading
import time
import uuid
from datetime import UTC, datetime

from kafka import KafkaProducer


def generate_uuid():
    return uuid.uuid4()


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    allow_auto_create_topics=True,
)


def load_coordinates(file_path: str):
    with open(file_path) as f:
        geo_data = json.load(f)
    return geo_data["features"][0]["geometry"]["coordinates"]


def produce_bus_data(busline: str, coordinates: list):
    i = 0
    data = {"busline": busline}

    while True:
        data["key"] = f"{busline}_{generate_uuid()}"
        data["timestamp"] = str(datetime.now(UTC))
        data["longitude"] = coordinates[i][0]
        data["latitude"] = coordinates[i][1]

        message = json.dumps(data)
        print(f"[{busline}] ->", message)

        producer.send("bus-coordinates", value=message.encode("utf-8"))
        i = (i + 1) % len(coordinates)
        time.sleep(1)


# Define buses with their files and buslines
bus_configs = [
    ("0001", "./geo-data/bus-geodata.json"),
    ("0002", "./geo-data/bus1-geodata.json"),
    ("0003", "./geo-data/bus2-geodata.json"),
]

# Launch each bus on a separate thread
threads = []
for busline, file_path in bus_configs:
    coords = load_coordinates(file_path)
    t = threading.Thread(target=produce_bus_data, args=(busline, coords), daemon=True)
    threads.append(t)
    t.start()

# Keep main thread alive
for t in threads:
    t.join()
