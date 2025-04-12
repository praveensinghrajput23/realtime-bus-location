from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from kafka import KafkaConsumer

app = FastAPI(debug=True, title="Bus Tracker", version="0.1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_kafka_consumer(topic_name: str):
    return KafkaConsumer(
        topic_name,
        bootstrap_servers="127.0.0.1:9092",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="fastapi-group",
    )


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"id": id}
    )


@app.get("/topic/{topic_name}")
async def get_messages(topic_name: str):
    def event_stream():
        consumer = get_kafka_consumer(topic_name)
        for message in consumer:
            yield f"data: {message.value.decode()}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", port=8001, reload=True)  # run with uvicorn
