import io
import json
from PIL import Image
from ws4py.client.threadedclient import WebSocketClient
from robot import say_with_emotion

EC2_WEBSOCKET = 'ws://ec2-54-197-14-241.compute-1.amazonaws.com:8765'

class Robot_Websocket(WebSocketClient):
    def __init__(self, image_filepath=None, websocket_address=EC2_WEBSOCKET):
        super(self.__class__, self).__init__(websocket_address)
        self.image_filepath = image_filepath

    def opened(self):
        if self.image_filepath is not None:
            with open(self.image_filepath, 'rb') as image:
                self.send(bytes(image.read()), binary=True)

    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def received_message(self, m):
        try:
            payload = json.loads(m.data)
            print('payload', payload)
            if m.completed and isinstance(payload, dict):
                if 'emotion' in payload and 'message' in payload:
                    say_with_emotion(
                        payload['message'],
                        payload['emotion'],
                    )
                else:
                    raise Exception('Invalid payload')
        except Exception, e:
            print 'ERROR:', m.data, str(e)

if __name__ == '__main__':
    try:
        ws = Robot_Websocket(image_filepath='camera_0.png')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
