from random import shuffle
from time import time


class Encryptor(object):
    def __init__(self, characters=None, backlog=-7):
        if characters is None:
            unicode_chars = []
            for i in range(1, 1028):
                unicode_chars.append(chr(i))
            self.characters = [c for c in unicode_chars]
            self.characters.remove('\r')
            self.characters.remove('\f')
            shuffle(self.characters)

        self.rev_ord = {}
        self.ord = {}

        self.range = len(self.characters)
        self.make_key(self.characters)
        self.mix = backlog

    def load_key_file(self, filepath='key'):
        with open(filepath, 'r') as f:
            key_data = f.read()
            self.characters = [c for c in key_data]
            self.make_key(self.characters)
        return self

    def save_key_file(self, filepath='key'):
        with open(filepath, 'w') as f:
            f.write(''.join(self.characters))
        return self

    def make_key(self, characters):
        if characters is not self.characters:
            self.characters = characters

        self.rev_ord = {}
        self.ord = {}

        for i, char in enumerate(self.characters):
            self.rev_ord[i+1] = char

        for key, value in self.rev_ord.items():
            self.ord[value] = key

        self.range = len(self.characters)
        return self

    def circular_add(self, start, amount):
        rng = (1, self.range)
        remainder = amount % rng[1]
        amount = remainder

        # Number is equally divisible and we can use the starting number
        if amount >= rng[1] and remainder == 0:
            return start

        # Amount is more than the range and there is a remainder.
        if amount >= rng[1] and remainder > 0:
            return start + remainder

        increase = start + amount
        if increase <= rng[1]:
            return increase

        if increase > rng[1]:
            return increase % rng[1]

    def circular_subtract(self, start, amount):
        rng = (1, self.range)
        remainder = amount % rng[1]
        amount = remainder

        if amount >= rng[1] and remainder == 0:
            return start

        if amount >= rng[1] and remainder > 0:
            return rng[1] - ((amount - start) % rng[1])

        if amount < rng[1] and start - amount < rng[0]:
            return rng[1] - (amount - start)

        if amount < rng[1] and start - amount >= rng[0]:
            return start - amount

    def encrypt(self, string):
        if not string:
            # raise ValueError("String cannot be empty.")
            return string

        first_letter_ord = self.ord[string[0]]
        output = ""

        for i, c in enumerate(string):
            c_ord = self.circular_add(self.ord[c], sum([self.ord[x] for x in string[:i][self.mix:]]))
            if i == 0:
                out = c
            else:
                _ = self.circular_add(first_letter_ord, c_ord)
                out = self.rev_ord[_]

            output += out
            first_letter_ord = self.ord[c]

        first_letter_number = self.circular_add(self.ord[string[0]], sum([self.ord[x] for x in output[self.mix:]]))

        output = self.rev_ord[first_letter_number] + output[1:]
        return output

    def decrypt(self, string):
        if not string:
            # raise ValueError("String cannot be empty.")
            return string

        first_letter_ord = self.ord[string[0]]
        if not first_letter_ord:
            raise ValueError("Your message is invalid.")

        output = ""

        # Set string's first letter to the correct un-encoded letter.
        first_letter_number = self.circular_subtract(first_letter_ord, sum([self.ord[x] for x in string[self.mix:]]))
        first_letter = self.rev_ord[first_letter_number]
        string = first_letter + string[1:]

        for i, c in enumerate(string):
            c_ord = self.circular_subtract(self.ord[c], sum([self.ord[x] for x in output[:i][self.mix:]]))

            if i == 0:
                out = c
            else:
                last_c_ord = self.ord[output[-1]]
                out_ord = self.circular_subtract(c_ord, last_c_ord)
                out = self.rev_ord[out_ord]

            output += out
            first_letter_ord = self.ord[out]

        return output


if __name__ == '__main__':
    s = Encryptor().load_key_file()

    print(''.join(s.characters))
    o = """hello hello hello hello hello hello
"""

    print('\nstring: {}'.format(len(o)), o)
    tstart = time()
    o = s.encrypt(o)
    end = time()
    entime = end - tstart
    print('\nencoded:', o)
    tstart = time()
    o = s.decrypt(o)
    end = time()
    untime = end - tstart
    print('\ndecoded:', o)

    print(entime)
    print(untime)
