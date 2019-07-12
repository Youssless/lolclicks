from LolRequest import LoLRequest
from pynput.mouse import Listener
import threading



count = 0
def main():
    ign = input ('[EUW1] LoL Username: ')
    
    with Listener(on_click=on_click) as listener:
        lolr = LoLRequest(ign, listener)
        lolr.handle_request()
        listener.join()
        


def on_click(x, y, button, pressed):
    global count
    if pressed:
        count = count + 1


if __name__ == "__main__":
    main()
