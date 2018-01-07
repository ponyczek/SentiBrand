from channels.routing import route, route_class
from dashboard.consumers import ws_connect, ws_disconnect, WsThread


channel_routing = [
    route('websocket.connect', ws_connect),
    route_class(WsThread),
    # route('websocket.receive', ws_receive),
    route('websocket.disconnect', ws_disconnect),

]