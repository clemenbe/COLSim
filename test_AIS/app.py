from flask import Flask, render_template
import asyncio
import websockets
import json
from datetime import datetime, timezone
import threading

app = Flask(__name__)

ship_positions = {}


async def connect_ais_stream():
    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {
            "APIKey": "0bbffae9f759d13fd5ae7161319d5a492c6364b1",
            # Coordinates for Melbourne Harbour
            "BoundingBoxes": [[[-11.190693542735469, 111.0005771472325], [-50.56548221020746, 175.6032904801916]]]
        }

        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
            if message["MessageType"] == "PositionReport":
                ais_message = message['Message']['PositionReport']
                ship_id = ais_message['UserID']
                latitude = ais_message['Latitude']
                longitude = ais_message['Longitude']
                ship_positions[ship_id] = {
                    'latitude': latitude,
                    'longitude': longitude,
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }


@app.route('/positions')
def positions():
    return json.dumps(ship_positions)


@app.route('/')
def index():
    return render_template('index.html')


def start_flask():
    app.run(debug=True, use_reloader=False)


if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    asyncio.run(connect_ais_stream())
