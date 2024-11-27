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
    def __init__(self, preamble: str = None):
        self.preamble = preamble if preamble else 'This sentence contains'

        self.counts: dict[str: int] = self.count_occurences(self.preamble)

        # options
        include_finanal_and = False

    @property
    def sentence(self) -> str:
        phrases = self.counts_as_phrases(self.counts)
        return f'{self.preamble} {", ".join(phrases[:-1])}, and {phrases[-1]}. '

    @property
    def is_autogram(self) -> bool:
        counts = self.count_occurences(self.sentence)
        return counts == self.counts

    def __getattr__(self, item):
        if item in string.ascii_lowercase:
            return self.counts[item]
        else:
            raise AttributeError(f"'Autogram' object has no attribute '{item}'")

    def count_occurences(self, s: str) -> dict:
        counts = defaultdict(int)
        for letter in string.ascii_lowercase:
            c = s.lower().count(letter)
            if c > 0:
                counts[letter] = c #+ 1  # +1? since stating the letter adds to it's count
        return counts

    def counts_as_phrases(self, counts: dict) -> list:
        return [f'''{num_2_words(count)} {letter}{"'s" * (count > 1)}'''
                for letter, count in counts.items() if count != 0]

    def update_counts(self):
        self.counts = self.count_occurences(self.sentence)
        # phrases = self.counts_as_phrases(self.counts)
        # self.intermediate_autogram = f'{self.preamble} {", ".join(phrases[:-1])}, and {phrases[-1]}. '

    def iter_sentence(self):
        current_sentence = self.sentence + ' '
        iter_counts = defaultdict(int)
        for letter in string.ascii_lowercase:
            new_count = current_sentence.lower().count(letter)

            new_sentence = current_sentence + f'''{num_2_words(c)} {letter}{"'s" * (c > 1)}, '''
            c_with_letter = new_sentence.lower().count(letter)



if __name__ == '__main__':
    ag = Autogram()
    print('counts:', ag.counts)
    print('sentence:', ag.sentence)
    print('autogram:', ag.is_autogram)

    print('\n--- update ---')
    ag.update_counts()
    print('counts:', ag.counts)
    print('sentence:', ag.sentence)
    print('autogram:', ag.is_autogram)
