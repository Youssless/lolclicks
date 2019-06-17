from pynput.mouse import Listener

count = 0

#f = open("num_clicks.log", "a")

def on_click(x, y, button, pressed):
    global count
    if pressed:
        count = count+1
        with open("num_clicks.txt", "w") as f:
            f.write(str(count))

with Listener(on_click = on_click) as listener:
    listener.join()

