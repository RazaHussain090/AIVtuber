
import websocket

def on_message(ws, message):
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("Connection opened")

    # Example: Send a simple request (adjust with a valid request for VTube Studio)
    request = '{"jsonrpc":"2.0","method":"APIMethodName","params":{"param1":"value1"},"id":1}'
    ws.send(request)

def run_websocket():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8001",  # Replace with the correct VTube Studio WebSocket URL
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
