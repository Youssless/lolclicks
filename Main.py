from LolRequest import LoLRequest
from pynput.mouse import Listener
import threading
import datetime as Date

count = 0

def main():
        #ign = input ('LoL Username: ')
        lolr = LoLRequest('Youssless')
        try:
        # listen for clicks when the game starts
                with Listener(on_click=on_click) as listener:
                # Thread to handle checking if the game has ended
                # While the main thread handles the click listener
                        handler = threading.Thread(target=lolr.handle_request, args=(listener,))
                        handler.start()
                        listener.join()        
        except KeyError:
                print("API key has expired or cannot be found, generate at:" 
                +" https://developer.riotgames.com/")


# function that handles when the user clicks on the mouse and counts them
def on_click(x, y, button, pressed):
    global count
    if pressed:
        count = count + 1


if __name__ == "__main__":
    main()
