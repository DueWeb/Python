import re
import random
from word_list import six_worded_list, five_worded_list, four_worded_list, eight_worded_list, seven_worded_list, three_worded_list
from tkinter import *


def welcome_options():
    print("\nWelcome to Hangman\n")
    print("1. " + "Noobie (10 lives)")
    print("2. " + "Intermediate (6 lives)")
    print("3. " + "Expert (3 lives)")


def game_setup():
    global max_life, wordList, word
    user_dif = input("\nChoose difficulty by number input.\n")
    if user_dif == "1":
        wordList = three_worded_list + four_worded_list
        max_life = 10
    elif user_dif == "2":
        wordList = five_worded_list + six_worded_list
        max_life = 6
    elif user_dif == "3":
        wordList = seven_worded_list + eight_worded_list
        max_life = 3
    else:
        print("\nThat is not a valid difficulty")
    word = random.choice(wordList)
    word = "butter"
    word = word.lower()


def check():
    life = max_life
    letters_in_word = [*word]
    print(letters_in_word)
    revealed_letters = [*(len(word)*'_')]
    guessed_letters = []

    while life > 0:
        guess = input("\nGuess the characters in the hidden word\n")
        guess = guess.lower()
        # google on enumerate to get index
        if guess in letters_in_word:
            for index, char in enumerate(letters_in_word):
                if guess == char:
                    revealed_letters.insert(index,char)
                    revealed_letters.pop(index+1)

        else:
            life -= 1
            guessed_letters.append(guess)
            print("You guessed wrong")
            print(guessed_letters)
        if life < 1:
            print("You have lost")
        if len(letters_in_word) == 0:
            print("you have won")
            break
        print(f'revealed letters: {revealed_letters}')



welcome_options()
game_setup()
check()
