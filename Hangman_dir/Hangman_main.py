# Imports
import random
import tkinter as tk
from tkinter import *
from tkinter import messagebox as msg
from tkinter import simpledialog
from tkinter.ttk import *

import tk_sleep
from network import connect, send

# Program function definitions


def main():  # main program loop
    global local_user

    local_user = simpledialog.askstring(
        'Input', 'Your username', parent=Hangman(tk.Tk)
    )

    channel = 'unique-channel-prefix' + simpledialog.askstring(
        'Input', 'channel to join', parent=Hangman(tk.Tk)
    )

    connect(channel=channel, user=local_user, handler=on_network_message)

# function that runs whenever we call send(message)


def on_network_message(timestamp, user: str, message: str):
    global text_box, game
    if user != local_user:  # ensures the textbox only gets updated by the network if you're not a local user
        print('writing')

        # appends whatever gets sent to the network to the textbox
        text_box.insert("end", message)


game_area = Frame()
message = Label(game_area, style='Message.TLabel')

three_worded_list = (
    "cat",
    "rat",
    "ink",
    "aid",
)

four_worded_list = (
    "java",
    "will",
)

five_worded_list = (
    "Brick",
    "Prick",
)

six_worded_list = (
    "Babies",
    "Cactus",
)

seven_worded_list = (
    "Abdomen",
    "Baboons",
)

eight_worded_list = (
    "Intellij",
    "Aardvark",
)

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
hang_font = ("Arial", 20)

game_state = {
    'me': None,
    'opponent': None,
    'is_server': None,
    'shared': {
        'who_is_playing': '',
        'word': '',
        'guessed_letters': [],
        'letters_in_word': [],
        'max_life': None,
        'game_over_message': '',
        'user_dif': ''
    }
}


def get_opponent_and_decide_game_runner(user, message):
    # who is the server (= the creator of the channel)
    if 'created the channel' in message:
        name = message.split("'")[1]
        game_state['is_server'] = name == game_state['me']

    # who is the opponent (= the one that joined that is not me)
    if 'joined channel' in message:
        name = message.split(' ')[1]
        if name != game_state['me']:
            game_state['opponent'] = name


def on_network_message(timestamp, user, message):
    if user == 'system':
        get_opponent_and_decide_game_runner(user, message)
    # shared state (only of interest to the none-server)
    if type(message) is dict and not game_state['is_server']:
        game_state['shared'] = message


class Hangman(tk.Tk):

    def __init__(self):
        self.welcome_options()
        self.user_dif = game_state['shared']['user_dif']
        self.max_life = game_state['shared']['max_life']
        while self.user_dif not in ["1", "2", "3"]:
            self.user_dif = input(
                "\nChoose difficulty by number input (press 0 to exit): ")
            if self.user_dif == "1":
                self.wordList = three_worded_list + four_worded_list
                self.max_life = 10
            elif self.user_dif == "2":
                self.wordList = five_worded_list + six_worded_list
                self.max_life = 6
            elif self.user_dif == "3":
                self.wordList = seven_worded_list + eight_worded_list
                self.max_life = 3
            elif self.user_dif == "0":
                print("exiting...")
                return
            else:
                print("\nThat is not a valid difficulty")
        super().__init__()
        self.draw_keyboard()
        self.setup_game()
        self.revealed_label = tk.Label(
            self, text=f"word : {self.revealed_letters}", font=hang_font)
        self.revealed_label.pack()
        self.lives_label = tk.Label(
            self, text=f" remaining tries: {self.life}", font=hang_font)
        self.lives_label.pack()

    def setup_game(self):
        self.word = game_state['shared']['word']
        self.letters_in_word = game_state['shared']['letters_in_word']
        self.guessed_letters = game_state['shared']['guessed_letters']
        self.life = game_state['shared']['max_life']
        self.word = random.choice(self.wordList)
        self.word = self.word.lower()
        self.letters_in_word = [*self.word]
        self.revealed_letters = [*(len(self.word)*'_')]
        self.guessed_letters = []
        self.life = self.max_life

    def welcome_options(self):
        print("\nWelcome to Hangman\n")
        print("1. " + "Noobie (10 lives)")
        print("2. " + "Intermediate (6 lives)")
        print("3. " + "Expert (3 lives)")

    def draw_keyboard(self):
        self.keyboard = tk.Toplevel()
        self.keyboard.geometry('800x200')
        n = 0
        for letter in letters:
            tk.Button(self.keyboard, text=letter, command=lambda guess=letter: self.check(guess),
                      font=('Helvetica 18'), width=4).grid(row=1+n//9, column=n % 9)
            n += 1

    def check(self, guess):
        if guess in self.letters_in_word:
            for index, char in enumerate(self.letters_in_word):
                if guess == char:
                    self.revealed_letters.insert(index, char)
                    self.revealed_letters.pop(index+1)

        else:
            self.life -= 1
            self.guessed_letters.append(guess)
            print("You guessed wrong")
            print(self.guessed_letters)
        if self.life < 1:
            msg.showerror(
                title=":(", message=f"You have lost the game, the word was {self.word}")
            self.setup_game()

        if self.letters_in_word == self.revealed_letters:
            msg.showinfo(title="congratulations", message="you have won")
            print(f'revealed letters: {self.revealed_letters}')
            self.setup_game()
        self.revealed_label.configure(text=f"word : {self.revealed_letters}")
        self.lives_label.configure(text=f" remaining tries: {self.life}")
        if game_state['shared']['who_is_playing'] == '':
            game_state['shared']['who_is_playing'] = game_state['me']
            game_state['shared']['word'] = self.word
            game_state['shared']['max_life'] = self.max_life
            game_state['shared']['user_dif'] = self.user_dif
            game_state['shared']['letters_in_word'] = self.letters_in_word
            send(game_state['shared'])
            h.mainloop()


local_user: str = None


def start():
    # hide some things initially
    ### j('.wait, .ball, .paddle-1, .paddle-2').hide()
    # show the content/body (hidden by css)
    # j('body').show()
    # connect to network
    game_state['me'] = simpledialog.askstring(
        'Input', 'Your user name', parent=Hangman)
    # note: adding prefix so I don't disturb
    # other class mates / developers using the same
    # network library
    channel = 'kevin_hang' + simpledialog.askstring(
        'Input', 'Channel', parent=Hangman)
    connect(channel, game_state['me'], on_network_message)
    message.config(text='Waiting for an opponent...')
    message.place(y=200, x=100)
    # wait for an opponent
    while game_state['opponent'] == None:
        tk_sleep(Hangman, 1 / 10)
    message.destroy()
    # start game loop if i am the server
    if game_state['is_server']:
        h.mainloop()


h = Hangman()
h.mainloop()

main()
