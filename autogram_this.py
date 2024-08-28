import string
from collections import defaultdict


NUM_WORDS = {
    '0': 'zero',
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine',

    '10': 'ten',
    '11': 'eleven',
    '12': 'twelve',
    '13': 'thirteen',
    '14': 'fourteen',
    '15': 'fifteen',
    '16': 'sixteen',
    '17': 'seventeen',
    '18': 'eighteen',
    '19': 'nineteen',

    '20': 'twenty',
    '30': 'thirty',
    '40': 'forty',
    '50': 'fifty',
    '60': 'sixty',
    '70': 'seventy',
    '80': 'eighty',
    '90': 'ninety',
    }


def num_2_words(num):
    """source: https://stackoverflow.com/a/78060953"""
    if num <= 20:
        return NUM_WORDS[str(num)]
    elif num % 10 == 0 and num < 100:
        return NUM_WORDS[str(num)]
    elif num < 100:
        return NUM_WORDS[str(num // 10) + '0'] + ' ' + NUM_WORDS[str(num % 10)]
    elif num % 100 == 0 and num < 1000:
        return NUM_WORDS[str(num // 100)] + ' ' + 'hundred'
    elif num < 1000:
        return NUM_WORDS[str(num // 100)] + ' hundred and ' + num_2_words(num % 100)
    elif num % 1000 == 0 and num < 10000:
        return NUM_WORDS[str(num // 1000)] + ' ' + 'thousand'
    elif num < 10000:
        return NUM_WORDS[str(num // 1000)] + ' thousand ' + num_2_words(num % 1000)
    elif num == 10000:
        return 'ten thousand'
    else:
        return 'more than ten thousand'


class Autogram(object):
    def __init__(self, preamble: str):
        self.preamble = preamble

        self.counts = self.count_occurences(self.preamble)
        self.intermediate_autogram = f'{self.preamble}'

    def count_occurences(self, s: str) -> dict:
        counts = defaultdict(int)
        for letter in string.ascii_lowercase:
            c = s.lower().count(letter)
            if c > 0:
                counts[letter] = c #+ 1  # +1 since stating the letter adds to it's count
        return counts

    def counts_as_phrases(self, counts: dict) -> list:
        return [f'''{num_2_words(count)} {letter}{"'s" * (count > 1)}'''
                for letter, count in counts.items() if count != 0]

    def update_counts(self):
        self.counts = self.count_occurences(self.intermediate_autogram)
        phrases = self.counts_as_phrases(self.counts)
        self.intermediate_autogram = f'{self.preamble} {", ".join(phrases[:-1])}, and {phrases[-1]}. '


if __name__ == '__main__':
    ag = Autogram('This sentence contains')
    ag.update_counts()
    print(ag.counts)
    print(ag.intermediate_autogram)

    print('--- update ---')
    ag.update_counts()
    print(ag.counts)
    print(ag.intermediate_autogram)
