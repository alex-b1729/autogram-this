import sys
import string
import random
from time import perf_counter
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
        return NUM_WORDS[str(num // 10) + '0'] + '-' + NUM_WORDS[str(num % 10)]
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
    """A class that helps search for autograms.

    ...

    Parameters
    ----------
    prefix : str, optional
        The string to start the autogram.
    suffix : str, optional
        The string that ends the autogram.

    Attributes
    ----------
    sentence : str
        Peroperty: A sentence generated using the current `counts` mapping.
    is_autogram : bool
        Property: True if `sentence` is an autogram
    make_plural : bool
        If True, appends a 's to the end of letters with count greater than 1. (default True)
    include_final_and : bool
        If True, add the word 'and' before the last letter count. (default True)
    is_pangram : bool
        If True, search for autograms where all letters of the alphabet are included. (default False)
    epoch : int
        The number of sentences tried during search.
    update_all_counts : bool
        If True, update all letter counts on next epoch, otherwise update one, random letter's count.
    counts : dict[str, int]
        Maps lower case letters to their count in the current sentence.
        Only includes letters with count > 0.

    Methods
    -------
    init_counts()
        Initiates the `count` attribute with the letter counts in `prefix + suffix`.
    counts_as_phrases(counts: dict) -> list
        Takes a mapping between letters to counts and outputs these counts as a comma
        delimited list with cardinal number names.
    count_occurrences(s: str) -> dict
        Take a string and returns a mapping from lowercase chars to their count in the sentence.
    update_counts()
        Updates the `counts` dictionary by alternatively updating all letters or one random letter
        as determined by the `update_all_counts` attribute.
    search()
        Repeatedly applies `update_counts()` until an autogram is found.
        Prints to stdout the initial sentence, the number of epochs (updated every 10,000),
        the time taken, the dictionary of letter to counts in the final solution, and the autogram.
    """
    def __init__(self, prefix: str = '', suffix: str = ''):
        self.prefix = prefix
        self.suffix = suffix

        self.epoch = 0
        self.update_all_counts = True

        # options
        self.make_plural = True
        self.include_final_and = True
        self.is_pangram = False
        # self.include_punctuation = False

        self.counts: dict[str, int] = defaultdict(int)

    def init_counts(self):
        if self.is_pangram:
            self.counts = {letter: 1 for letter in string.ascii_lowercase}
        else:
            if self.prefix or self.suffix:
                self.counts = self.count_occurrences(self.prefix + self.suffix)
            else:
                self.counts = defaultdict(int)
                self.counts[random.choice(string.ascii_lowercase)] += 1

    def counts_as_phrases(self, counts: dict) -> list:
        return [f'''{num_2_words(count)} {letter}{"'s" * (count > 1) if self.make_plural else ''}'''
                for letter, count in counts.items() if count != 0]

    @property
    def sentence(self) -> str:
        phrases = self.counts_as_phrases(self.counts)
        s = self.prefix + ' ' if self.prefix else ''
        s += ", ".join(phrases[:-1])
        if self.include_final_and:
            s += ', and ' + phrases[-1]
        else:
            s += ', ' + phrases[-1]
        if self.suffix:
            s += ', ' + self.suffix
        elif self.prefix:
            s += '.'
        return s

    @property
    def is_autogram(self) -> bool:
        counts = self.count_occurrences(self.sentence)
        return counts == self.counts

    def count_occurrences(self, s: str) -> dict:
        return {
            letter: s.lower().count(letter)
            for letter in string.ascii_lowercase
            if s.lower().find(letter) != -1
        }

    def update_counts(self):
        # Lee Sallows suggests alternately updating all letter counts or a random letter's count
        if self.update_all_counts:
            self.counts = self.count_occurrences(self.sentence)
        else:
            letter = random.choice(list(self.counts.keys()))
            self.counts[letter] = self.sentence.lower().count(letter)
        self.update_all_counts = not self.update_all_counts
        self.epoch += 1

    def search(self):
        self.init_counts()
        self.epoch = 0
        sys.stdout.write(f'Iterating sentences to find an {"autogram" if not self.is_pangram else "pangram"}\n')
        sys.stdout.write(f'Starting sentence: {self.sentence}\n')
        print_epoch_counter = 0
        t0 = perf_counter()

        while not self.is_autogram:
            self.update_counts()
            if print_epoch_counter > 9998:
                sys.stdout.write(f'\rEpoch: {self.epoch:,}')
                print_epoch_counter = -1
            print_epoch_counter += 1

        t1 = perf_counter()
        t = t1 - t0
        sys.stdout.write(f'\rEpoch: {self.epoch:,}\n')
        sys.stdout.write('Found an autogram!\n')
        sys.stdout.write(f'Total time: {t // 60:.0f} minutes {t % 60:.0f} seconds\n')
        sys.stdout.write(f'Raw count dictionary: {self.counts}\n')
        sys.stdout.write(f'\n{self.sentence}\n\n')
        return self.sentence


if __name__ == '__main__':
    ag = Autogram('Spam, Spam, Spam,', 'eggs, and Spam.')
    ag.include_final_and = False
    ag.search()
