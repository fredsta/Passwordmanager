# passwd_gen.py
# author, version = fredsta, 19.09.2021
# Basic password-generator

import random
import string
from intputs import input_functions, generators


class passwd_gen:
    def __init__(self):
        self.length = 0
        self.include_capitals = False
        self.include_extra_chars = False        


    def parameter_prompt(self):
        """Asks the user for parameters of the password e.g. length or type of characters"""
        self.length = int(input("Length (8-16)? "))
        self.include_capitals = input_functions.yes_or_no_prompt("Include Capitals?")
        self.include_extra_chars = input_functions.yes_or_no_prompt("Extra characters (!,?,:, etc.)?")


    def generate_chars(self):
        # determine how many capital and extra_chars are going into the password
        count_capital = 0
        count_extra = 0
        password = ""
        if self.include_capitals:
            count_capital = random.randint(1, self.length-1)
        if self.include_extra_chars:
            count_extra = random.randint(1, self.length-1)
        while count_extra + count_capital >= self.length:
            count_extra -= 1
            count_capital -= 1

        count_lower = self.length - count_capital - count_extra  # how many 'normal' letters there will be
        capitals = generators.generate_capitals(count_capital)
        special_chars = generators.generate_extras(count_extra)
        lower_cases = generators.generate_lower(count_lower)

        passwd_ingredients = capitals + lower_cases + special_chars
        for i in range(self.length):
            x = random.randint(0, len(passwd_ingredients)-1)
            to_append = passwd_ingredients.pop(x)
            password = password + to_append
        return password


    def generate_password(self, length = 8, include_capitals = True, include_extras = True):
        self.length = length
        self.include_capitals = include_capitals
        self.include_extra_chars = include_extras
        password = self.generate_chars()
        return password


if __name__ == '__main__':
    generator = passwd_gen()
    for i in range(10):
        print(generator.generate_password())