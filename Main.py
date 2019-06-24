import LolRequest
import time
from pynput.mouse import Listener
import threading
import datetime as Date

count = 0

def main():
    try:
        code = LolRequest.handle_request()
        
        # listen for clicks when the game starts
        if code == 200:
                with Listener(on_click=on_click) as listener:
                        # Thread to handle checking if the game has ended
                        # While the main thread handles the click listener
                        checker = threading.Thread(target=check_game_state, args=(code,listener))
                        checker.start()
                        listener.join()        
    except KeyError:
        print("API key has expired or cannot be found, generate at:" 
         +" https://developer.riotgames.com/")


# as long as the player is in game the method will keep on checking
# if the player is in game
# function handles terminating the program
def check_game_state(code, listener):
    while code == 200:
        check = LolRequest.check_ig(code)
        # sleep as the amount of requests to the api is limited
        time.sleep(10)
        # False return from check means the game has ended hence stop listening for events
        if check == False:    
            print("Game ended, terminating...")    
            listener.stop()
            curr_time = Date.datetime.now()

            with open("num_clicks.log", "a") as f:
                f.write(curr_time.strftime("[%d/%m/%Y %H:%M:%S] ") + str(count) + " clicks")
                f.write("\n")
            break

# function that handles when the user clicks on the mouse and counts them
def on_click(x, y, button, pressed):
    global count
    if pressed:
        count = count + 1


if __name__ == "__main__":
    main()
