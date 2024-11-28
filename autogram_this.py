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
    def __init__(self, preamble: str = None):
        self.preamble = preamble

        self.epoch = 0
        self.update_all_counts = True

        # options
        self.make_plural = True
        self.include_final_and = True
        self.is_pangram = False
        # self.include_punctuation = False

        if self.is_pangram:
            self.counts = {letter: 1 for letter in string.ascii_lowercase}
        else:
            if self.preamble:
                self.counts = self.count_occurences(self.preamble)
            else:
                self.counts = defaultdict(int)
                self.counts['g'] += 1

    def counts_as_phrases(self, counts: dict) -> list:
        return [f'''{num_2_words(count)} {letter}{"'s" * (count > 1) if self.make_plural else ''}'''
                for letter, count in counts.items() if count != 0]

    @property
    def sentence(self) -> str:
        phrases = self.counts_as_phrases(self.counts)
        s = self.preamble + ' ' if self.preamble else ''
        s += ", ".join(phrases[:-1])
        if self.include_final_and:
            s += ' and ' + phrases[-1]
        else:
            s += ', ' + phrases[-1]
        return s

    @property
    def is_autogram(self) -> bool:
        counts = self.count_occurences(self.sentence)
        return counts == self.counts

    def count_occurences(self, s: str) -> dict:
        return {
            letter: s.lower().count(letter)
            for letter in string.ascii_lowercase
            if s.lower().find(letter) != -1
        }

    def update_counts(self):
        # Lee Sallows suggests alternately updating all letter counts or a random letter's count
        if self.update_all_counts:
            self.counts = self.count_occurences(self.sentence)
        else:
            letter = random.choice(list(self.counts.keys()))
            self.counts[letter] = self.sentence.lower().count(letter)
        self.update_all_counts = not self.update_all_counts
        self.epoch += 1

    def iter_sentences(self):
        sys.stdout.write('Iterating sentences to find an autogram.\n')
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
        sys.stdout.write(f'{self.sentence}\n')
        sys.stdout.write(f'Raw count dictionary: {self.counts}\n')
        sys.stdout.write(f'Total time: {t//60:.0f} minutes {t%60:.0f} seconds\n')


if __name__ == '__main__':
    ag = Autogram('This sentence contains')
    ag.iter_sentences()
