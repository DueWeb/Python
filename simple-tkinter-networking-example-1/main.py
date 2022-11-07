# Imports
import tkinter as tk
from tkinter import simpledialog
from network import connect, send


# Program function definitions
def main():  # main program loop
    global local_user

    local_user = simpledialog.askstring(
        'Input', 'Your username', parent=window
    )

    channel = 'unique-channel-prefix' + simpledialog.askstring(
        'Input', 'channel to join', parent=window
    )

    connect(channel=channel, user=local_user, handler=on_network_message)


# function that runs whenever we call send(message)
def on_network_message(timestamp, user: str, message: str):
    global text_box, game

    if user != local_user:  # ensures the textbox only gets updated by the network if you're not a local user
        print('writing')

        # appends whatever gets sent to the network to the textbox
        text_box.insert("end", message)


def input(event):  # function for handling keyboard events
    print(event)
    key = event.keysym
    # sends message to the network, which gets handled by the on_network_message function
    send(key)


# Application
window = tk.Tk()
local_user: str = None

window.geometry('800x800')  # set window size
text_box = tk.Text()  # instantiate textbox
text_box.pack()  # add textbox to parent widget

window.bind_all("<Key>", input)  # bind keyboard events to the input function

main()  # run main function

window.mainloop()  # start tkinter gui application
