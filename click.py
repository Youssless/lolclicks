from pynput.mouse import Listener
count=0

# function that handles when the user clicks on the mouse
def on_click(x, y, button, pressed):
    global count
    if pressed:
        count=count+1
        # write the clicks to a file
        with open("num_clicks.txt", "w") as f:
            f.write(str(count))

def listen():
    with Listener(on_click = on_click) as listener:
        listener.join()
    


