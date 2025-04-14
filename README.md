# Realtime Bus Location

## Overview
This project is a real-time bus tracking application built with FastAPI. It consumes bus location data from a Kafka topic and serves it to a web interface.

## Prerequisites
- Docker
- UV (python package manager)


## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone <repository-url>
cd realtime-bus-location
```

### 2. Start Kafka with Docker
Make sure you have Docker installed. You can start a Kafka container using the following command:
```bash
docker pull apache/kafka:4.0.0
docker run -p 9092:9092 apache/kafka:4.0.0
```

### 3. Install Dependencies

Make sure you have [uv](https://github.com/astral-sh/uv) installed.

To set up your environment and install all dependencies:

```bash
uv venv                     # Creates a virtual environment in .venv/
source .venv/bin/activate   # On Windows use .venv\Scripts\activate
uv sync                     # Installs all dependencies from pyproject.toml and poetry.lock

### 4. Start the Producer
Run the `producer.py` script to start sending bus location data to Kafka:
```bash
python producer.py
```

### 5. Start the FastAPI Application
Run the FastAPI application using Uvicorn:
```bash
python app.py
```

### 6. Access the Application
Open your web browser and navigate to:
```
http://localhost:8001
```

### 7. View Bus Data
You can access the bus data by navigating to:
```
http://localhost:8001/topic/bus-coordinates
```

## Project Structure
- `app.py`: The main FastAPI application.
- `producer.py`: The Kafka producer that sends bus location data.
- `geo-data/`: Contains JSON files with bus geolocation data.
- `static/`: Contains static files like JavaScript libraries.
- `templates/`: Contains HTML templates for rendering the web interface.
- `pyproject.toml`: Project dependencies and metadata.

## License
This project is licensed under the MIT License.

