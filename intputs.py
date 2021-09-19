#Bibliothek für einige Input-Funktionen, die einem das Leben erleichtern sollen.

import random
import string

class input_functions:
    def yes_or_no_prompt(question):
        """asks the user for a certain question and returns a bool"""
        prompt = question + " (j/n)"
        answer = input(prompt)
        if answer == "j":
            return True
        elif answer == "n":
            return False
        else:
            raise("Fehler bei der Eingabe [Possible inputs were 'j' or 'n']")

    def intput():
        """basic function to quickly get a number from the user"""
        number = None
        try:
            number = int(input("Bitte eine Zahl eingeben: "))
            return number
        except Exception:
            return -1

class generators:
    def generate_extras(number):
        """Generates random extra characters and puts them into extras"""
        extras = []
        extra_characters = "0123456789!#$%&()*+,-./:;<=>?@_"
        for i in range(number):
            letter = random.randint(0, 30)
            extras.append(extra_characters[letter])
        return extras

    def generate_capitals(number):
        """Generates random capital letters and puts them into capitals"""
        capitals = []
        for i in range (number):
            letter = random.randint(0, 25)
            capitals.append(string.ascii_uppercase[letter])
        return capitals

    def generate_lower(number):
        """Generates random lowercase letters and puts them into the list lower_cases"""
        lower_cases = []
        for i in range(number):
            letter = random.randint(0, 25)
            lower_cases.append(string.ascii_lowercase[letter])
        return lower_cases
