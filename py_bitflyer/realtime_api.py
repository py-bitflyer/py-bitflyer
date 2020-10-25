import json
import threading
import time
import websocket
from logging import getLogger


class RealtimeAPI(object):
    """
    Realtime API (JSON-RPC 2.0 over WebSocket)

    https://bf-lightning-api.readme.io/docs/realtime-api
    """

    def __init__(self, channel, data_queue, is_daemon=False):
        self.logger = getLogger(__name__)
        self.ws = None
        self.running = False
        self.end_point = 'wss://ws.lightstream.bitflyer.com/json-rpc'
        self.channel = channel
        self.data_queue = data_queue
        self.is_daemon = is_daemon

    def on_open(self):
        self.logger.info('WebSocket connected')
        self.subscribe()

    def on_close(self):
        self.logger.info('WebSocket disconnected')

    def on_message(self, message):
        messages = json.loads(message)
        if 'method' not in messages or messages['method'] != 'channelMessage':
            return

        messages = messages['params']['message']
        for message in messages:
            self.data_queue.put(message)

    def on_error(self, error):
        self.logger.error(error)

    def subscribe(self):
        self.ws.send(json.dumps({'method': 'subscribe', 'params': {'channel': self.channel}}))

    def run(self):
        while self.running:
            try:
                self.ws = websocket.WebSocketApp(
                    self.end_point,
                    on_open=self.on_open,
                    on_close=self.on_close,
                    on_message=self.on_message,
                    on_error=self.on_error)
                self.ws.run_forever()
            except Exception as e:
                self.logger.error(e)
            time.sleep(3)

    def start(self):
        self.logger.info('Start streaming')
        self.running = True
        thread = threading.Thread(target=self.run, daemon=self.is_daemon)
        thread.start()

    def stop(self):
        self.logger.info('Stop streaming')
        self.running = False
        self.ws.close()
