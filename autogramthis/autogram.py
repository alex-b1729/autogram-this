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


LETTER_CHARS = string.ascii_lowercase
PUNCTUATION_CHARS = ',-\'.!'
CHAR_TO_WORD = {letter: letter for letter in LETTER_CHARS}
CHAR_TO_WORD.update({
    ',': 'comma',
    '-': 'hyphen',
    '\'': 'apostrophe',
    '.': 'period',
    # below inconsistent with above but used to validate Sallow's autogram
    # with punctuation from Hofstadter's 1982 "Metamagical Themas"
    '!': '!',
})
WORD_TO_CHAR = {letter: letter for letter in LETTER_CHARS}
WORD_TO_CHAR.update({
    'comma': ',',
    'hyphen': '-',
    'apostrophe': '\'',
    'period': '.',
    '!': '!',
})


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
        self.include_punctuation = False

        self.countable_chars = LETTER_CHARS

        self.counts: dict[str, int] = defaultdict(int)

    def init_counts(self):
        if self.is_pangram:
            self.counts = {letter: 1 for letter in LETTER_CHARS}
        else:
            if self.prefix or self.suffix:
                self.counts = self.count_occurrences(self.prefix + self.suffix)
            else:
                self.counts = defaultdict(int)
                self.counts[random.choice(LETTER_CHARS)] += 1

    def init_countable_chars(self):
        self.countable_chars = LETTER_CHARS
        if self.include_punctuation:
            self.countable_chars += PUNCTUATION_CHARS

    def counts_as_phrases(self, counts: dict[str, int]) -> list[str]:
        return [f'''{num_2_words(count)} {CHAR_TO_WORD[char]}{"'s" * (count > 1) if self.make_plural else ''}'''
                for char, count in counts.items() if count != 0]

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

    def count_occurrences(self, s: str) -> dict[str, int]:
        return {
            char: s.lower().count(char)
            for char in self.countable_chars
            if s.lower().find(char) != -1
        }

    def update_counts(self):
        # Lee Sallows suggests alternately updating all letter counts or a random letter's count
        if self.update_all_counts:
            self.counts = self.count_occurrences(self.sentence)
        else:
            char = random.choice(list(self.counts.keys()))
            self.counts[char] = self.sentence.lower().count(char)
        self.update_all_counts = not self.update_all_counts
        self.epoch += 1

    def search(self):
        self.init_countable_chars()
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
    def find_counts_and_chars(
            sentence: str,
            include_punctuation: bool = False,
            verbose: bool = False,
    ) -> list[tuple[str, str]]:
        """Uses regex to match descriptions of a number of letters.
        E.g. "Twenty-two t's", "five b", "thirty one s"
        todo: only works for numbers < 100
        """
        # number words that can stand on their own. e.g. 'two', 'thirteen', 'thirty', ...
        single_word_numbers = [word for word in WORD_TO_INT]
        # e.g. 'twenty', 'fifty'
        leading_word_numbers = [word for word in WORD_TO_INT if WORD_TO_INT[word] >= 20]
        leading_word_or = '|'.join(leading_word_numbers)
        single_word_or = '|'.join(single_word_numbers)

        # 0 or 1 of (leading word followed by a '-' or whitespace), followed by one single word
        number_re = fr'(?P<number>(?:(?:{leading_word_or})[-\s]?)?(?:{single_word_or}))'

        # one char from a-z, followed by 0 or 1 of "'" only if thats followed by an 's',
        # followed by 0 or 1 's'
        punctuation_re = ''
        if include_punctuation:
            punctuation_or = '|'.join([
                punct_word for punct_word in WORD_TO_CHAR
                if punct_word not in string.ascii_lowercase
            ])
            punctuation_re = punctuation_or + '|'
        char_re = fr'(?P<letter>(?:{punctuation_re}[a-z])' + '{1}' + fr")'?(?=s)?s?"

        # find a word break, followed by a number word match, followed by whitespace,
        # followed by a letter match
        number_char_re = fr'\b{number_re}\s{char_re}'

        p = re.compile(number_char_re)
        return p.findall(sentence.lower())

    @staticmethod
    def validate(
            sentence,
            include_punctuation: bool = False,
            verbose: bool = False,
            double_verbose: bool = False,
    ) -> bool:
        """Returns True if sentence is an autogram"""
        sentence_lower = sentence.lower()
        if double_verbose and not verbose:
            verbose = True
        countable_chars = LETTER_CHARS
        if include_punctuation:
            countable_chars += PUNCTUATION_CHARS
        counts = {
            char: sentence_lower.count(char)
            for char in countable_chars
            if sentence_lower.count(char) > 0
        }

        # find sentence char counts
        counts_and_chars = Autogram.find_counts_and_chars(sentence_lower, include_punctuation=include_punctuation)

        # create dictionary of letter counts as described by sentence
        sentence_counts = {}
        for match in counts_and_chars:
            num_match = match[0]
            char_match = match[1]
            sentence_counts[WORD_TO_CHAR[char_match]] = words_2_num(num_match)

        if double_verbose:
            print(f'Regex sentence counts: {counts_and_chars}')
            print(f'Parsed sentence counts: {sentence_counts}')
            print(f'function counts: {counts}')

        # compare function counts to sentence counts
        valid = True
        for char in counts:
            if char in sentence_counts:
                sc = sentence_counts.pop(char)
                if counts[char] == sc:
                    if verbose: print(f'{char}: {sc} verified')
                else:
                    valid = False
                    print(f'{char}: INVALID. True count: {counts[char]}, Sentence says: {sc}.')
            else:
                valid = False
                print(f'{char}: Missing from sentence. True count: {counts[char]}.')
        # any remaining letters that were mentioned by the sentence by somehow
        # not found in the function counts mean the function didn't pick up on something it should've
        if sentence_counts:
            raise RuntimeError(
                f'Sentence mentions {len(sentence_counts)} chars that were not found by validate().\n'
                f'{sentence_counts}'
            )

        return valid


def run_validation_tests():
    # first element is sentence, second is whether punctuation is counted
    sentences: list[tuple[str, bool]] = [
        ("""Spam, Spam, Spam, six a's, two d's, twenty e's, seven f's, four g's,
        five h's, ten i's, two l's, five m's, seven n's, six o's, five p's,
        six r's, thirty-one s's, twelve t's, three u's, eight v's, five w's,
        four x's, three y's, eggs, and Spam.""", False),
        ("""twenty e, four f, one g, five h, three i, one l, ten n, seven o,
        seven r, three s, nine t, three u, four v, three w, one x, two y""", False),
        ("""The output of this Python script is composed of two a's, three c's,
        three d's, thirty-one e's, nine f's, three g's, ten h's, twelve i's,
        two l's, two m's, fourteen n's, fourteen o's, five p's, eight r's,
        twenty-seven s's, twenty-five t's, five u's, eight v's, seven w's,
        one x, and five y's.""", False),
        ("""This sentence contains three a's, three c's, two d's, twenty-seven e's,
        four f's, one g, five h's, eleven i's, two l's, sixteen n's, seven o's,
        five r's, twenty-nine s's, sixteen t's, two u's, six v's, six w's, six x's,
        and three y's.""", False),
        ("""The quick brown fox jumped over alphabet soup containing five a's, three b's,
        three c's, three d's, thirty-two e's, six f's, two g's, ten h's, twelve i's,
        two j's, two k's, three l's, two m's, sixteen n's, sixteen o's, four p's,
        two q's, thirteen r's, thirty-four s's, twenty-seven t's, seven u's, seven v's,
        ten w's, six x's, four y's, and one z.""", False),
        ("""Only the fool would take trouble to verify that his sentence was composed 
        of ten a's, three b's, four c's, four d's, forty-six e's, sixteen f's, 
        four g's, thirteen h's, fifteen i's, two k's, nine l's, four m's, 
        twenty-five n's, twenty-four o's, five p's, sixteen r's, forty-one s's, 
        thirty-seven t's, ten u's, eight v's, eight w's, four x's, eleven y's, 
        twenty-seven commas, twenty-three apostrophes, seven hyphens and, last but 
        not least, a single !""", True),  # A Lee Sallow autogram
    ]
    for i, sentence in enumerate(sentences):
        print(f'\n----------------- sentence {i + 1} -----------------')
        print(sentence[0])
        is_valid = Autogram.validate(
            sentence[0],
            include_punctuation=sentence[1],
        )
        print('Valid!' if is_valid else 'Invalid!')


if __name__ == '__main__':
    run_validation_tests()
