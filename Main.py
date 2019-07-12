from LolRequest import LoLRequest
from pynput.mouse import Listener
import threading

ign = input ('[EUW1] LoL Username: ')
lolr = LoLRequest(ign, None)
handler = threading.Thread(target=lolr.handle_request)
handler.start()


def on_click(x, y, button, pressed):
    if pressed:
        lolr.count = lolr.count + 1

with Listener(on_click=on_click) as listener:
    lolr.listener = listener
    listener.join()
#if __name__ == "__main__":
#    main()
