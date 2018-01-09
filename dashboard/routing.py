from channels.routing import route, route_class
from dashboard.consumers import ws_connect, ws_disconnect, ws_receive


channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.receive', ws_receive),
    # route_class(WsThread),
    route('websocket.disconnect', ws_disconnect),
]