import time

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from kafka import KafkaConsumer
from kafka.errors import KafkaError

app = FastAPI(debug=True, title="Bus Tracker", version="0.1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"id": id}
    )


@app.get("/topic/{topic_name}")
async def get_messages(topic_name: str):
    def event_stream():
        try:
            # Retry logic if Kafka is not ready
            retries = 5
            while retries > 0:
                try:
                    consumer = KafkaConsumer(
                        topic_name,
                        bootstrap_servers="127.0.0.1:9092",
                        auto_offset_reset="latest",
                        enable_auto_commit=True,
                        group_id="fastapi-group",
                        consumer_timeout_ms=10000,  # <-- allows the loop to exit cleanly if no data
                    )
                    break
                except KafkaError:
                    print(f"Kafka not ready yet... retrying ({5 - retries}/5)")
                    retries -= 1
                    time.sleep(2)
            else:
                yield 'data: {"error": "Kafka unavailable"}\n\n'
                return

            # Continuously stream data from Kafka
            for message in consumer:
                yield f"data: {message.value.decode()}\n\n"

        except Exception as e:
            print("Exception in event stream:", e)
            yield f'data: {{"error": "{str(e)}"}}\n\n'

    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", port=8001, reload=True)  # run with uvicorn
