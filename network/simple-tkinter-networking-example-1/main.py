# Imports
from tkinter import *
import tkinter as tk
from tkinter import simpledialog
from network import connect, send
from string import ascii_lowercase
from hangman.word_list import three_worded_list, four_worded_list, five_worded_list, six_worded_list, seven_worded_list, eight_worded_list
from hangman import word_list

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
window.title=("Hangman")
photos = [
    PhotoImage(file="Skrivbord/hello-python/Hangman_img/hang0.png"), PhotoImage(file="Skrivbord/hello-python/Hangman_img/hang1.png"),
    PhotoImage(file="Skrivbord/hello-python/Hangman_img/hang2.png"), PhotoImage(file="Skrivbord/hello-python/Hangman_img/hang3.png"),
    PhotoImage(file="Skrivbord/hello-python/Hangman_img/hang4.png"), PhotoImage(file="Skrivbord/hello-python/Hangman_img/hang5.png"), 
    PhotoImage(file="Skrivbord/hello-python/Hangman_img/hang6.png"), PhotoImage(file="Skrivbord/hello-python/Hangman_img/hang7.png"), 
    PhotoImage(file="Skrivbord/hello-python/Hangman_img/hang8.png"), PhotoImage(file="Skrivbord/hello-python/Hangman_img/hang9.png"), 
    PhotoImage(file="Skrivbord/hello-python/Hangman_img/hang10.png"), PhotoImage(file="Skrivbord/hello-python/Hangman_img/hang11.png")]

imgLabel = Label(window)
imgLabel.grid(row=0, column=0, columnspan=3, padx=10, pady=40)
imgLabel.config(image=photos[0])

lblWord=Stringvar()
Label(window, textvariable=lblWord)



n=0
for i in ascii_lowercase:
    Button(window, text=i, command=lambda i=i: guess(i), font=("Arial 14"), width=4).grid(row=1+n//9, column=n%9)
    n+=1

local_user: str = None

window.geometry('800x800')  # set window size
text_box = tk.Text()  # instantiate textbox
text_box.pack()  # add textbox to parent widget

window.bind_all("<Key>", input)  # bind keyboard events to the input function

main()  # run main function

window.mainloop()  # start tkinter gui application
