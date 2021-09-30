# collection of some useful functions for the generator
# author: fredsta
# version: 30.09.2021

import random
import string


class input_functions:
    # asks the user for a certain question and returns a bool
    def yes_or_no_prompt(question):
        prompt = question + " (j/n)"
        answer = input(prompt)
        if answer == "j":
            return True
        elif answer == "n":
            return False
        else:
            raise("Error on input [Possible inputs were 'j' or 'n']")

    #basic function to quickly get a number from the user
    def intput():
        number = None
        try:
            number = int(input("Please insert a number: "))
            return number
        except Exception:
            return -1

class generators:
    # Generates random extra characters and puts them into extras
    def generate_extras(number):
        extras = []
        extra_characters = "0123456789!#$%&()*+,-./:;<=>?@_"  # not complete but for passwords acceptable
        for i in range(number):
            letter = random.randint(0, 30)
            extras.append(extra_characters[letter])
        return extras

    #Generates random capital letters and puts them into capitals
    def generate_capitals(number):
        capitals = []
        for i in range (number):
            letter = random.randint(0, 25)
            capitals.append(string.ascii_uppercase[letter])
        return capitals

    # Generates random lowercase letters and puts them into the list lower_cases
    def generate_lower(number):
        lower_cases = []
        for i in range(number):
            letter = random.randint(0, 25)
            lower_cases.append(string.ascii_lowercase[letter])
        return lower_cases