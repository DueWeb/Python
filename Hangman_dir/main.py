# Imports
from tkinter import *
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
photos = [
    #PhotoImage(file="/Users/KevinSundberg/Desktop/hello-python/Python/Hangman_dir/Hangman_img/hang0.png"),
    #PhotoImage(file="/Users/KevinSundberg/Desktop/hello-python/Python/Hangman_dir/Hangman_img/hang1.png"),
    #PhotoImage(file="/Users/KevinSundberg/Desktop/hello-python/Python/Hangman_dir/Hangman_img/hang2.png"),
    #PhotoImage(file="/Users/KevinSundberg/Desktop/hello-python/Python/Hangman_dir/Hangman_img/hang3.png"),
    #PhotoImage(file="/Users/KevinSundberg/Desktop/hello-python/Python/Hangman_dir/Hangman_img/hang4.png"),
    #PhotoImage(file="/Users/KevinSundberg/Desktop/hello-python/Python/Hangman_dir/Hangman_img/hang5.png"),
    #PhotoImage(file="/Users/KevinSundberg/Desktop/hello-python/Python/Hangman_dir/Hangman_img/hang6.png"),
    #PhotoImage(file="/Users/KevinSundberg/Desktop/hello-python/Python/Hangman_dir/Hangman_img/hang7.png"),
    #PhotoImage(file="/Users/KevinSundberg/Desktop/hello-python/Python/Hangman_dir/Hangman_img/hang8.png"),
    #PhotoImage(file="/Users/KevinSundberg/Desktop/hello-python/Python/Hangman_dir/Hangman_img/hang9.png"),
    #PhotoImage(file="/Users/KevinSundberg/Desktop/hello-python/Python/Hangman_dir/Hangman_img/hang10.png"),
    #PhotoImage(file="/Users/KevinSundberg/Desktop/hello-python/Python/Hangman_dir/Hangman_img/hang11.png"),
    PhotoImage(file="./Hangman_img/hang11.png")
]

def guess_char(event):
    char = 'a' # get the text from the button that was pressed
    print(event)
    word_widget.config(text=char)
    send(char)

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

local_user: str = None


window.geometry('800x800')  # set window size
frame = tk.Frame()  # instantiate textbox
word_text = len('butter')*'_ '

word_widget = tk.Label(frame,text=word_text)
word_widget.pack()
#word_widget.config(text=) this sets the text in the label to whatever is after text=

for letter in letters:
    button = tk.Button(frame,text=letter)
    button.bind('click',guess_char)
    button.pack()

frame.pack()  # add textbox to parent widget

window.bind_all("<Key>", input)  # bind keyboard events to the input function

main()  # run main function

window.mainloop()  # start tkinter gui application
