from random import SystemRandom
from time import time


class Encryptor(object):
    def __init__(self, characters=None, backlog=-1):
        self.random = SystemRandom()
        if characters is None:
            unicode_chars = [chr(i) for i in range(1, 1028)]
            self.characters = [c for c in unicode_chars]
            self.characters.remove('\r')
            self.characters.remove('\f')
            self.random.shuffle(self.characters)

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

    def increment(self, start, amount):
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

    def decrement(self, start, amount):
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

        mix = 0
        for i, c in enumerate(string):
            increase = sum([self.ord[x] for x in string[:i][self.mix:]])
            c_ord = self.increment(self.ord[c], increase + mix)
            mix += increase
            if i == 0:
                out = c
            else:
                _ = self.increment(first_letter_ord, c_ord)
                out = self.rev_ord[_]

            output += out
            first_letter_ord = self.ord[c]

        first_letter_number = self.increment(self.ord[string[0]], sum([self.ord[x] for x in output[self.mix:]]))

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
        first_letter_number = self.decrement(first_letter_ord, sum([self.ord[x] for x in string[self.mix:]]))
        first_letter = self.rev_ord[first_letter_number]
        string = first_letter + string[1:]

        mix = 0
        for i, c in enumerate(string):
            increase = sum([self.ord[x] for x in output[:i][self.mix:]])
            c_ord = self.decrement(self.ord[c], increase + mix)
            mix += increase

            if i == 0:
                out = c
            else:
                last_c_ord = self.ord[output[-1]]
                out_ord = self.decrement(c_ord, last_c_ord)
                out = self.rev_ord[out_ord]

            output += out
            first_letter_ord = self.ord[out]

        return output


if __name__ == '__main__':
    s = Encryptor().load_key_file()

    print(''.join(s.characters))
    o = """A super awesome possum, gathered cherry blossoms, while in a rush he lost them.
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
A super awesome possum, gathered cherry blossoms, while in a rush he lost them. 
"""

    print('\nstring: {}'.format(len(o)), o)
    tstart = time()
    o = s.encrypt(o)
    print('utf-8:', o.encode('utf-8'))
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
