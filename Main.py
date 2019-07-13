from LolRequest import LoLRequest
from pynput.mouse import Listener
import threading


ign = input ('[EUW1] LoL Username: ')
lolr = LoLRequest(ign, None)
# thread for printing the check while mouse listener runs on a seperate thread
handler = threading.Thread(target=lolr.handle_request)

# event for clicking a mouse button
def on_click(x, y, button, pressed):
    if pressed:
        lolr.count = lolr.count + 1

# listens for the event
with Listener(on_click=on_click) as listener:
    lolr.listener = listener
    handler.start()
    listener.join()
#if __name__ == "__main__":
#    main()
