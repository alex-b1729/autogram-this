import re
import sys
import string
import random
from time import perf_counter
from collections import defaultdict


INT_TO_WORD = {
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

WORD_TO_INT = {
    'zero': 0,
    'single': 1,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,

    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,

    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,
}


def num_2_words(num: int) -> str:
    """source: https://stackoverflow.com/a/78060953"""
    if num <= 20:
        return INT_TO_WORD[str(num)]
    elif num % 10 == 0 and num < 100:
        return INT_TO_WORD[str(num)]
    elif num < 100:
        return INT_TO_WORD[str(num // 10) + '0'] + '-' + INT_TO_WORD[str(num % 10)]
    elif num % 100 == 0 and num < 1000:
        return INT_TO_WORD[str(num // 100)] + ' ' + 'hundred'
    elif num < 1000:
        return INT_TO_WORD[str(num // 100)] + ' hundred and ' + num_2_words(num % 100)
    elif num % 1000 == 0 and num < 10000:
        return INT_TO_WORD[str(num // 1000)] + ' ' + 'thousand'
    elif num < 10000:
        return INT_TO_WORD[str(num // 1000)] + ' thousand ' + num_2_words(num % 1000)
    elif num == 10000:
        return 'ten thousand'
    else:
        return 'more than ten thousand'


def words_2_num(words: str) -> int:
    # todo: parse words of nums > 99
    word_list = [w.lower() for w in re.split(r'[-\s]+', words)]
    if len(word_list) > 2:
        raise NotImplementedError(
            f'Cannot yet parse number words of greater than 2 words. {word_list} is too long.'
        )
    num = 0
    for w in word_list:
        num += WORD_TO_INT[w]
    return num


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

    @staticmethod
    def validate(
            sentence,
            include_punctuation: bool = False,
            verbose: bool = False,
    ) -> bool:
        sentence_lower = sentence.lower()
        counts = {
            letter: sentence_lower.count(letter)
            for letter in string.ascii_lowercase
            if sentence_lower.count(letter) > 0
        }

        # find sentence letter counts with regex
        letter_count_re = r"\b(?P<number>[efghilnorstuvwxy]+[-\s]?[efghilnorstuvwxy]+)\s(?P<letter>[a-z]{1})\b'?(?=s)?s?[,\.]?"
        p = re.compile(letter_count_re)
        letter_count_iter = p.finditer(sentence_lower)

        # create dictionary of letter counts as described by sentence
        sentence_counts = {}
        for match in letter_count_iter:
            num_word = match.group('number')
            # regex sometimes finds an extra, non-number word as the first word
            # e.g. "(of two) (a)'s"
            # if num_word[0] not in WORD_TO_INT:
            #     num_word = num_word[1:]
            sentence_counts[match.group('letter')] = words_2_num(num_word)

        # compare function counts to sentence counts
        valid = True
        incorrect_counts = {}
        missing_counts = {}
        # letters in the order they appear in sentence
        for letter in counts:
            if letter in sentence_counts:
                sc = sentence_counts.pop(letter)
                if counts[letter] == sc:
                    if verbose: print(f'{letter}: {sc} verified')
                else:
                    valid = False
                    print(f'{letter}: INVALID. True count: {counts[letter]}, Sentence says {sc}')
                    incorrect_counts[letter] = sc
            else:
                valid = False
                print(f'{letter}: Missing from sentence. True count {counts[letter]}')
        # any remaining letters that were mentioned by the sentence by somehow
        # not found in the function counts
        if sentence_counts:
            raise RuntimeError(
                f'Sentence mentions {len(sentence_counts)} that were not found by function.\n{sentence_counts}'
            )

        return valid




if __name__ == '__main__':
    sentences = [
        """Spam, Spam, Spam, six a's, two d's, twenty e's, seven f's, four g's, 
        five h's, ten i's, two l's, five m's, seven n's, six o's, five p's, 
        six r's, thirty-one s's, twelve t's, three u's, eight v's, five w's, 
        four x's, three y's, eggs, and Spam.""",
        """twenty e, four f, one g, five h, three i, one l, ten n, seven o, 
        seven r, three s, nine t, three u, four v, three w, one x, two y""",
        """The output of this Python script is composed of two a's, three c's, 
        three d's, thirty-one e's, nine f's, three g's, ten h's, twelve i's, 
        two l's, two m's, fourteen n's, fourteen o's, five p's, eight r's, 
        twenty-seven s's, twenty-five t's, five u's, eight v's, seven w's, 
        one x, and five y's.""",
        """This sentence contains three a's, three c's, two d's, twenty-seven e's, 
        four f's, one g, five h's, eleven i's, two l's, sixteen n's, seven o's, 
        five r's, twenty-nine s's, sixteen t's, two u's, six v's, six w's, six x's, 
        and three y's.""",
        """The quick brown fox jumped over alphabet soup containing five a's, three b's, 
        three c's, three d's, thirty-two e's, six f's, two g's, ten h's, twelve i's, 
        two j's, two k's, three l's, two m's, sixteen n's, sixteen o's, four p's, 
        two q's, thirteen r's, thirty-four s's, twenty-seven t's, seven u's, seven v's, 
        ten w's, six x's, four y's, and one z.""",
    ]
    for i, sentence in enumerate(sentences):
        print(f'\n----------------- sentence {i+1} -----------------')
        print(sentence)
        is_valid = Autogram.validate(sentence, verbose=True)
        print('Valid!' if is_valid else 'Invalid!')
