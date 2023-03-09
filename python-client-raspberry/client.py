from twisted.internet import ssl, reactor
from twisted.internet.protocol import ReconnectingClientFactory
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory
import json

class MyClientProtocol(WebSocketClientProtocol):
    def onConnect(self, response):
        print(f"Connected to server: {response.peer}")

    def onOpen(self):
        print("WebSocket connection open.")
        self.sendMessage("Hello, world!".encode('utf8'))

    def onMessage(self, payload, isBinary):
        # print(f"Received message: {payload.decode('utf8')}")

        json_data = json.loads(payload.decode('utf8'))
        
        print(f"Datos Recibidos: {json.dumps(json_data, indent=2)}")
        print("-"*100)

    def onClose(self, wasClean, code, reason):
        print(f"WebSocket connection closed: {reason}")


class MyClientFactory(WebSocketClientFactory, ReconnectingClientFactory):
    protocol = MyClientProtocol

    def __init__(self, url):
        WebSocketClientFactory.__init__(self, url)
        self.setProtocolOptions(autoPingInterval=10, autoPingTimeout=5)

    def clientConnectionFailed(self, connector, reason):
        print(f"Connection failed: {reason}")
        self.retry(connector)

    def clientConnectionLost(self, connector, reason):
        print(f"Connection lost: {reason}")
        self.retry(connector)


if __name__ == '__main__':
    factory = MyClientFactory(u"wss://api.gemini.com/v1/marketdata/BTCUSD")
    contextFactory = ssl.ClientContextFactory()
    reactor.connectSSL(factory.host, factory.port, factory, contextFactory)
    reactor.run()