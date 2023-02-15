from aiohttp import web
import socketio
import ssl

ROOM = 'room'

"""
   Certificados wildcard a *.iesvalledeljerteplasencia.es
   Rutas en servidor -----
"""
SSLCertificateFile    = "/etc/certies/iesvalledeljerteplasencia.es_ssl_certificate.cer"
SSLCertificateKeyFile = "/etc/certies/_.iesvalledeljerteplasencia.es_private_key.key"

sio = socketio.AsyncServer(cors_allowed_origins='*', ping_timeout=35)
app = web.Application()
sio.attach(app)



# Create an SSL context
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(SSLCertificateFile, SSLCertificateKeyFile)

@sio.event
async def connect(sid, environ):
    print('Connected', sid)
    await sio.emit('ready', room=ROOM, skip_sid=sid)
    sio.enter_room(sid, ROOM)


@sio.event
def disconnect(sid):
    sio.leave_room(sid, ROOM)
    print('Disconnected', sid)


@sio.event
async def data(sid, data):
    print('Message from {}: {}'.format(sid, data))
    await sio.emit('data', data, room=ROOM, skip_sid=sid)


if __name__ == '__main__':
    web.run_app(app, port=9999, ssl_context=ssl_context)

